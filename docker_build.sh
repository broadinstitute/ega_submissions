#!/bin/bash
set -e

# Update version when changes to Dockerfile are made
IMAGE_VERSION=0.0.1
TIMESTAMP=$(date +"%s")

# Environment variables
DOCKER_REGISTRY_URL="us-east1-docker.pkg.dev"
PROJECT_ID="sc-ega-submissions"
REPOSITORY_NAME="ega-submission-scripts"
IMAGE_NAME="python-scripts"
GAR_URL="$DOCKER_REGISTRY_URL/$PROJECT_ID/$REPOSITORY_NAME/$IMAGE_NAME"
IMAGE_TAG="$IMAGE_VERSION-$TIMESTAMP"

# Check if required environment variables are set
if [ -z "$DOCKER_REGISTRY_URL" ]; then
    echo "Error: DOCKER_REGISTRY_URL is not set."
    exit 1
fi

# Check if the user is authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" &> /dev/null; then
    echo "Error: You are not authenticated with gcloud. Please run 'gcloud auth login' to authenticate."
    exit 1
fi


# Log the build and push process
echo "Building Google Artifact Image - $GAR_URL:$IMAGE_TAG"
docker build --platform linux/amd64 -t "$GAR_URL:$IMAGE_TAG" . || { echo "Docker build failed"; exit 1; }

echo "Pushing Google Artifact Image - $GAR_URL:$IMAGE_TAG"
docker push "$GAR_URL:$IMAGE_TAG" || {
  echo "Docker push failed";
  echo "Run 'gcloud auth configure-docker us-east1-docker.pkg.dev' to ensure authentication."
  exit 1;
}

echo "Google Artifact Image pushed successfully"
