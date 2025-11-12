#!/bin/bash
set -e

# Install base requirements
pip install -r requirements.txt

# Install b0-data-models from GitHub
# If GITHUB_TOKEN is set, use it for authentication
if [ -n "$GITHUB_TOKEN" ]; then
    echo "Installing b0-data-models with GitHub token..."
    # Use token in URL format for private repos
    pip install git+https://${GITHUB_TOKEN}@github.com/Base0ai/b0-data-models.git
else
    echo "Warning: GITHUB_TOKEN not set. Attempting to install b0-data-models as public repo..."
    pip install git+https://github.com/Base0ai/b0-data-models.git || {
        echo "Error: Failed to install b0-data-models. Please set GITHUB_TOKEN environment variable for private repositories."
        exit 1
    }
fi

