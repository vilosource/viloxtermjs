# CI Docker Image

This repository uses a custom Docker image for CI/CD to speed up test runs by pre-installing all system dependencies.

## Image Details

- **Registry**: GitHub Container Registry (ghcr.io)
- **Image**: `ghcr.io/vilosource/viloxtermjs-ci:latest`
- **Base**: Ubuntu 24.04
- **Python versions**: 3.11 and 3.12
- **Pre-installed**: All Qt/PySide6 system dependencies, xvfb, test tools

## Benefits

- **Faster CI**: Reduces setup time from ~60 seconds to ~5 seconds
- **Consistent environment**: Same dependencies across all runs
- **Cost efficient**: Less GitHub Actions minutes consumed

## Building the Image

The image is automatically built and pushed when:
1. Changes are made to `.github/Dockerfile.ci`
2. The workflow is manually triggered
3. Weekly schedule (Sundays at midnight UTC) for security updates

To manually trigger a rebuild:
1. Go to Actions tab
2. Select "Build CI Docker Image"
3. Click "Run workflow"

## Local Testing

To test with the same environment as CI locally:

```bash
# Pull the image
docker pull ghcr.io/vilosource/viloxtermjs-ci:latest

# Run tests in container
docker run --rm -v $(pwd):/workspace \
  ghcr.io/vilosource/viloxtermjs-ci:latest \
  bash -c "cd /workspace && pip install -e .[test] && pytest tests/"
```

## Updating the Image

To add new system dependencies:
1. Edit `.github/Dockerfile.ci`
2. Commit and push to main or develop
3. The image will automatically rebuild

## Fallback

The test workflow includes a fallback job that installs dependencies normally if the Docker image is unavailable.