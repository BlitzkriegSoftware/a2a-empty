# Demo of environmental configuration and validation

Rules:

1. Don't hard code configurations
2. Make configurations rule based
3. Provide sane defaults for non-required values
4. Have a set of validators (min/max) or (regex)
5. Have settings self document in form of validation json

## Run tests w. coverage

From the root of this demo project (the one with `pyproject.toml` in it)

```powershell
uv run pytest --cov=./src --cov-report html
```
