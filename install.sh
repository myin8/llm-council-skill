#!/bin/bash
# LLM Council Skill Installer
# Usage: bash install.sh

set -e

INSTALL_DIR="${HOME}/s/llm-council-skill"
REPO_URL="https://github.com/yourusername/llm-council-skill"  # Update with actual repo URL

echo "=================================================="
echo "  LLM Council Skill Installer"
echo "=================================================="
echo ""

# Check if directory exists
if [ -d "${INSTALL_DIR}" ]; then
    echo "✓ Directory exists at ${INSTALL_DIR}"
    echo "  Updating to latest version..."
    cd "${INSTALL_DIR}"
    git pull
else
    echo "→ Cloning repository to ${INSTALL_DIR}..."
    git clone "${REPO_URL}" "${INSTALL_DIR}"
    cd "${INSTALL_DIR}"
fi

echo ""
echo "→ Setting up environment file..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✓ Created .env file"
    echo ""
    echo "⚠️  IMPORTANT: You need to add your OpenRouter API key!"
    echo "   Edit ${INSTALL_DIR}/.env and add:"
    echo "   OPENROUTER_API_KEY=your_key_here"
    echo ""
    echo "   Get a key from: https://openrouter.ai/keys"
    NEEDS_KEY=1
else
    echo "✓ .env file already exists"
    NEEDS_KEY=0
fi

echo ""
echo "→ Installing dependencies..."
if command -v uv &> /dev/null; then
    uv sync
    echo "✓ Dependencies installed with uv"
else
    echo "⚠️  uv not found, using pip..."
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    echo "✓ Dependencies installed with pip"
    echo "   Activate with: source ${INSTALL_DIR}/.venv/bin/activate"
fi

echo ""
echo "=================================================="
echo "  Installation Complete!"
echo "=================================================="
echo ""

if [ $NEEDS_KEY -eq 1 ]; then
    echo "⚠️  NEXT STEP: Add your API key to .env"
    echo ""
    echo "1. Get your key from: https://openrouter.ai/keys"
    echo "2. Edit ${INSTALL_DIR}/.env"
    echo "3. Add: OPENROUTER_API_KEY=your_key_here"
    echo ""
fi

echo "Test the installation:"
echo "  cd ${INSTALL_DIR}"
echo "  uv run python council_run.py 'What is 2+2?' --stages 1"
echo ""
echo "Use from Claude Code:"
echo "  Ask the council: <your question>"
echo "  /llm-council"
echo ""
