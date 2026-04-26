#!/usr/bin/env bash
# Manual smoke test for the data science template.
# Creates a throwaway project, installs dependencies, and exercises core utilities.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="$(dirname "$SCRIPT_DIR")"
TIMESTAMP="$(date +%Y%m%d%H%M%S)"
PROJECT_NAME="ds-template-smoke-${TIMESTAMP}"
PROJECT_PATH="${TARGET_DIR}/${PROJECT_NAME}"

if ! command -v uv >/dev/null 2>&1; then
    echo "❌ The 'uv' package manager is required. Install it from https://docs.astral.sh/uv/ before running the smoke test."
    exit 1
fi

cleanup() {
    if [ -d "$PROJECT_PATH" ]; then
        rm -rf "$PROJECT_PATH"
        echo "🧹 Removed temporary project at $PROJECT_PATH"
    fi
}
trap cleanup EXIT

echo "🚦 Starting manual smoke test..."
"${SCRIPT_DIR}/new-ds-project.sh" "$PROJECT_NAME"

pushd "$PROJECT_PATH" >/dev/null

echo "🔄 Syncing dependencies with uv..."
uv sync

echo "🧪 Importing template utilities..."
uv run python -c "from utils import quick_info; print('Template utilities import check ✅')"

popd >/dev/null

echo "✅ Smoke test complete. Template is healthy."
