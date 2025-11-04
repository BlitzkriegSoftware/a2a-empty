# One-Time Setup Script
#!/bin/bash
set -e

PROJECT_ID="your-project-id"
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")
REPO="your-org/your-repo"

gcloud services enable iam.googleapis.com run.googleapis.com cloudbuild.googleapis.com

gcloud iam workload-identity-pools create github-pool \
  --location="global" \
  --display-name="GitHub Pool"

gcloud iam workload-identity-pools providers create-oidc github \
  --location="global" \
  --workload-identity-pool="github-pool" \
  --display-name="GitHub Provider" \
  --attribute-mapping="attribute.repository=assertion.repository,attribute.actor=assertion.actor" \
  --issuer-uri="https://token.actions.githubusercontent.com"

gcloud iam service-accounts create github-deployer \
  --display-name="GitHub OIDC Deployer"

gcloud iam service-accounts add-iam-policy-binding github-deployer@$PROJECT_ID.iam.gserviceaccount.com \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/$PROJECT_NUMBER/locations/global/workloadIdentityPools/github-pool/attribute.repository/$REPO"
