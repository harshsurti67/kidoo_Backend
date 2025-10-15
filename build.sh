#!/usr/bin/env bash
# Build script for Render.com deployment (root wrapper)

set -euo pipefail

# Ensure backend build script runs (installs backend/requirements_render.txt)
chmod +x backend/build.sh
backend/build.sh
