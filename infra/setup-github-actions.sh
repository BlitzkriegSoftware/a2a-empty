#!/bin/bash
# GitHub Actions Setup Script for Cloud Run Deployment
# This script automates the Workload Identity Federation setup

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration - UPDATE THESE VALUES
PROJECT_ID="${PROJECT_ID:-your-project-id}"
GITHUB_REPO="${GITHUB_REPO:-your-username/a2a-empty}"
REGION="${REGION:-us-central1}"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}GitHub Actions Setup for Cloud Run${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Validate inputs
if [ "$PROJECT_ID" = "your-project-id" ]; then
    echo -e "${RED}Error: Please set PROJECT_ID environment variable${NC}"
    echo "Usage: PROJECT_ID=your-project-id GITHUB_REPO=username/repo ./setup-github-actions.sh"
    exit 1
fi

if [ "$GITHUB_REPO" = "your-username/a2a-poc" ]; then
    echo -e "${RED}Error: Please set GITHUB_REPO environment variable${NC}"
    echo "Usage: PROJECT_ID=your-project-id GITHUB_REPO=username/repo ./setup-github-actions.sh"
    exit 1
fi

echo -e "${YELLOW}Configuration:${NC}"
echo "  Project ID: $PROJECT_ID"
echo "  GitHub Repo: $GITHUB_REPO"
echo "  Region: $REGION"
echo ""

# Set project
echo -e "${YELLOW}Setting GCP project...${NC}"
gcloud config set project $PROJECT_ID

# Get project number
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")
echo -e "${GREEN} Project Number: $PROJECT_NUMBER${NC}"
echo ""

# Enable APIs
echo -e "${YELLOW}Step 1: Enabling required APIs...${NC}"
gcloud services enable \
  cloudbuild.googleapis.com \
  run.googleapis.com \
  containerregistry.googleapis.com \
  artifactregistry.googleapis.com \
  secretmanager.googleapis.com \
  iam.googleapis.com \
  iamcredentials.googleapis.com \
  sts.googleapis.com

echo -e "${GREEN} APIs enabled${NC}"
echo ""

# Create Workload Identity Pool
# Using 'github-actions-pool' to avoid conflict with soft-deleted 'github-pool'
echo -e "${YELLOW}Step 2: Creating Workload Identity Pool...${NC}"
if gcloud iam workload-identity-pools describe github-actions-pool --location=global --project=$PROJECT_ID &>/dev/null; then
  echo -e "${GREEN} Pool already exists${NC}"
else
  if gcloud iam workload-identity-pools create github-actions-pool \
    --location="global" \
    --display-name="GitHub Actions Pool" \
    --project=$PROJECT_ID; then
    echo -e "${GREEN} Pool created${NC}"
  else
    echo -e "${RED} Failed to create pool${NC}"
    exit 1
  fi
fi
echo ""

# Create OIDC Provider
echo -e "${YELLOW}Step 3: Creating OIDC Provider...${NC}"
if gcloud iam workload-identity-pools providers describe github-provider \
  --location=global \
  --workload-identity-pool=github-actions-pool \
  --project=$PROJECT_ID &>/dev/null; then
  echo -e "${GREEN} Provider already exists${NC}"
else
  # Using minimal configuration first to avoid attribute condition errors
  if gcloud iam workload-identity-pools providers create-oidc github-provider \
    --location="global" \
    --workload-identity-pool="github-actions-pool" \
    --display-name="GitHub Provider" \
    --attribute-mapping="google.subject=assertion.sub,attribute.repository=assertion.repository,attribute.actor=assertion.actor,attribute.repository_owner=assertion.repository_owner" \
    --attribute-condition="assertion.repository_owner == '${GITHUB_REPO%%/*}'" \
    --issuer-uri="https://token.actions.githubusercontent.com" \
    --project=$PROJECT_ID; then
    echo -e "${GREEN} Provider created${NC}"
  else
    echo -e "${RED} Failed to create provider${NC}"
    echo -e "${YELLOW}Trying fallback creation method (minimal config)...${NC}"
   
    # Fallback: Create with minimal config then update
    if gcloud iam workload-identity-pools providers create-oidc github-provider \
      --location="global" \
      --workload-identity-pool="github-actions-pool" \
      --issuer-uri="https://token.actions.githubusercontent.com" \
      --attribute-mapping="google.subject=assertion.sub" \
      --project=$PROJECT_ID; then
     
      echo -e "${GREEN} Provider created (minimal)${NC}"
      echo -e "${YELLOW}Updating provider attributes...${NC}"
     
      gcloud iam workload-identity-pools providers update-oidc github-provider \
        --location="global" \
        --workload-identity-pool="github-actions-pool" \
        --attribute-mapping="google.subject=assertion.sub,attribute.repository=assertion.repository,attribute.actor=assertion.actor,attribute.repository_owner=assertion.repository_owner" \
        --attribute-condition="assertion.repository_owner == '${GITHUB_REPO%%/*}'" \
        --project=$PROJECT_ID
       
      echo -e "${GREEN} Provider updated${NC}"
    else
      echo -e "${RED} Failed to create provider. Please create manually in GCP Console.${NC}"
      exit 1
    fi
  fi
fi
echo ""

# Create service account for GitHub Actions
echo -e "${YELLOW}Step 4: Creating GitHub deployer service account...${NC}"
gcloud iam service-accounts create github-deployer \
  --display-name="GitHub Actions Deployer" \
  --project=$PROJECT_ID 2>/dev/null && echo -e "${GREEN}✓ Service account created${NC}" || echo -e "${GREEN} Service account already exists${NC}"
echo ""

# Grant permissions to GitHub deployer
echo -e "${YELLOW}Step 5: Granting permissions to GitHub deployer...${NC}"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:github-deployer@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/cloudbuild.builds.editor" \
  --condition=None > /dev/null

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:github-deployer@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/run.admin" \
  --condition=None > /dev/null

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:github-deployer@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/storage.admin" \
  --condition=None > /dev/null

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:github-deployer@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/iam.serviceAccountUser" \
  --condition=None > /dev/null

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:github-deployer@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor" \
  --condition=None > /dev/null

echo -e "${GREEN}✓ Permissions granted${NC}"
echo ""

# Bind Workload Identity
echo -e "${YELLOW}Step 6: Binding Workload Identity to service account...${NC}"
gcloud iam service-accounts add-iam-policy-binding \
  github-deployer@$PROJECT_ID.iam.gserviceaccount.com \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/$PROJECT_NUMBER/locations/global/workloadIdentityPools/github-actions-pool/attribute.repository/$GITHUB_REPO" \
  --project=$PROJECT_ID > /dev/null

echo -e "${GREEN} Workload Identity bound${NC}"
echo ""

# Create Cloud Run service account if it doesn't exist
echo -e "${YELLOW}Step 7: Setting up Cloud Run service account...${NC}"
SA_EXISTS=$(gcloud iam service-accounts describe cloudrun-agent-sa@$PROJECT_ID.iam.gserviceaccount.com 2>/dev/null)

if [ -z "$SA_EXISTS" ]; then
  gcloud iam service-accounts create cloudrun-agent-sa \
    --display-name="Cloud Run Agent Service Account" \
    --project=$PROJECT_ID
 
  echo "Waiting for service account to propagate..."
  sleep 10
fi

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:cloudrun-agent-sa@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor" \
  --condition=None > /dev/null

# Allow Cloud Build to act as Cloud Run service account
gcloud iam service-accounts add-iam-policy-binding \
  cloudrun-agent-sa@$PROJECT_ID.iam.gserviceaccount.com \
  --member="serviceAccount:$PROJECT_NUMBER@cloudbuild.gserviceaccount.com" \
  --role="roles/iam.serviceAccountUser" > /dev/null

echo -e "${GREEN} Cloud Run service account configured${NC}"
echo ""

# Output GitHub secrets
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Setup Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${YELLOW}Add these secrets to your GitHub repository:${NC}"
echo -e "${YELLOW}(Settings → Secrets and variables → Actions → New repository secret)${NC}"
echo ""
echo -e "${GREEN}Secret Name: WIF_PROVIDER${NC}"
echo "projects/$PROJECT_NUMBER/locations/global/workloadIdentityPools/github-actions-pool/providers/github-provider"
echo ""
echo -e "${GREEN}Secret Name: WIF_SERVICE_ACCOUNT${NC}"
echo "github-deployer@$PROJECT_ID.iam.gserviceaccount.com"
echo ""
echo -e "${GREEN}Secret Name: GCP_PROJECT_ID${NC}"
echo "$PROJECT_ID"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Add the above secrets to your GitHub repository"
echo "2. Commit and push the workflow file: .github/workflows/deploy-cloudrun.yaml"
echo "3. Push to 'dev' or 'main' branch to trigger deployment"
echo "4. Or manually trigger from GitHub Actions tab"
echo ""
