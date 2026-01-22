# ==============================================================================
# INSTRUCTION: UPDATING ENVIRONMENT AFTER CHANGING PYPROJECT.TOML
# Purpose: Fix the "uv.lock needs to be updated" error during Docker builds.
# Use this when you swap packages (e.g., psycopg2 -> psycopg2-binary in pyproject.toml).
# ==============================================================================

# STEP 1: Synchronize the lockfile (uv.lock) with pyproject.toml.
# Run this every time you manually add or remove a package from [dependencies].
uv lock

# STEP 2: (Optional) Refresh your local virtual environment (.venv).
# This ensures your local Python environment matches what Docker will have.
uv sync

# STEP 3: Re-run your Docker build script.
# Now 'uv sync --locked' inside the Dockerfile will pass successfully 
# because the lockfile is perfectly aligned with your dependencies.
.\commands\2_1_docker_build_postgress_run_ingestion_script.ps1

# ==============================================================================
# WHY IS THIS NECESSARY?
# 1. Removing/Adding a package makes pyproject.toml newer than uv.lock.
# 2. Docker uses the --locked flag, which forbids 'uv' from changing the lockfile.
# 3. 'uv lock' updates the file locally so it can be safely copied into the image.
# ==============================================================================