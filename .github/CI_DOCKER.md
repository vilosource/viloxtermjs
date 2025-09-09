# CI Docker Image Documentation

## Purpose and Clarification

**IMPORTANT**: This Docker image is **ONLY for CI/CD testing**, not for building or distributing the viloxtermjs project.

- **viloxtermjs** remains a normal Python package that users install with `pip install viloxtermjs`
- The Docker image is just a "pre-configured test environment" to speed up GitHub Actions
- End users never need or see this Docker image

## Why Use a CI Docker Image?

### Without Docker CI:
Every test run must:
1. Install Ubuntu packages (~30 seconds)
2. Install Python versions (~10 seconds)  
3. Install test dependencies (~20 seconds)
4. Run tests

**Total: ~60 seconds of setup per test run**

### With Docker CI:
1. Pull pre-built image (~5 seconds)
2. Run tests

**Total: ~5 seconds of setup per test run**

### Savings Example:
- 100 test runs without Docker: 100 × 60s = 100 minutes
- 100 test runs with Docker: 100 × 5s = 8.3 minutes
- **Time saved: ~91 minutes per 100 runs**

## When is the Docker Image Built?

The Docker image is **NOT** rebuilt on every push. It's ONLY built when:

1. **Dockerfile changes** - You edit `.github/Dockerfile.ci`
2. **Workflow changes** - You edit `.github/workflows/docker-ci-image.yml`
3. **Manual trigger** - You manually run the "Build CI Docker Image" workflow
4. **Weekly schedule** - Automatic rebuild every Sunday at midnight UTC for security updates

### Normal Development Flow:
```
Push code to develop → Tests run using EXISTING Docker image (no rebuild)
Push code to main    → Tests run using EXISTING Docker image (no rebuild)
Edit Dockerfile.ci   → Docker image rebuilds ONCE
Next 100+ pushes     → All use the cached image (5 seconds each)
```

## Image Details

- **Registry**: GitHub Container Registry (ghcr.io)
- **Image**: `ghcr.io/vilosource/viloxtermjs-ci:latest`
- **Base**: Ubuntu 24.04
- **Python versions**: 3.11 and 3.12 (via deadsnakes PPA)
- **Pre-installed**: 
  - All Qt/PySide6 system dependencies
  - Xvfb for headless testing
  - pytest, pytest-qt, pytest-cov
  - black, flake8, mypy

## Manual Rebuild

To manually trigger a Docker image rebuild:
1. Go to the [Actions tab](https://github.com/vilosource/viloxtermjs/actions)
2. Select "Build CI Docker Image" workflow
3. Click "Run workflow"
4. Select branch and click "Run workflow" button

## Local Testing with CI Environment

To test locally with the exact same environment as CI:

```bash
# Pull the CI image
docker pull ghcr.io/vilosource/viloxtermjs-ci:latest

# Run tests in container (same as CI)
docker run --rm -v $(pwd):/workspace \
  ghcr.io/vilosource/viloxtermjs-ci:latest \
  bash -c "cd /workspace && pip install -e .[test] && pytest tests/"

# Interactive shell in CI environment
docker run --rm -it -v $(pwd):/workspace \
  ghcr.io/vilosource/viloxtermjs-ci:latest \
  bash
```

## Adding New System Dependencies

If you need to add new system packages for testing:

1. Edit `.github/Dockerfile.ci`
2. Add your packages to the `apt-get install` list
3. Commit and push (to main or develop)
4. The image will automatically rebuild (only when Dockerfile changes)
5. All future test runs will have the new dependencies

## Fallback Mechanism

The test workflow includes a fallback job that runs if the Docker image is unavailable:
- This ensures tests can still run even if the Docker registry is down
- The fallback installs all dependencies from scratch (slower but reliable)
- You'll see "test-fallback" job run if the main test job fails to pull the image

## Cost Savings

Using this CI Docker image saves:
- **GitHub Actions minutes**: ~55 seconds per test run
- **Developer time**: Faster feedback on pull requests
- **Resources**: Less CPU/bandwidth used for package installation

For a project with 20 test runs per day:
- Monthly savings: ~550 minutes (9+ hours) of GitHub Actions time
- Yearly savings: ~6,600 minutes (110 hours) of GitHub Actions time