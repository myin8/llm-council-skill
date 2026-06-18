#!/bin/sh
# LLM Council Skill Installer
# Usage: ./install.sh [--install-dir DIR] [--help]

set -eu

INSTALL_DIR="${LLM_COUNCIL_INSTALL_DIR:-$HOME/.local/share/llm-council-skill}"
NON_INTERACTIVE="${LLM_COUNCIL_NON_INTERACTIVE:-false}"
REPO_URL="https://github.com/myin8/llm-council-skill"

step() {
  printf '==> %s\n' "$1"
}

warn() {
  printf 'WARNING: %s\n' "$1" >&2
}

parse_args() {
  while [ "$#" -gt 0 ]; do
    case "$1" in
      --install-dir)
        if [ "$#" -lt 2 ]; then
          echo "--install-dir requires a value." >&2
          exit 1
        fi
        INSTALL_DIR="$2"
        shift
        ;;
      --help | -h)
        cat <<EOF
Usage: install.sh [--install-dir DIR]

Install the LLM Council skill for Claude Code.

Options:
  --install-dir DIR    Install to DIR instead of default location
  --help, -h           Show this help message

Environment variables:
  LLM_COUNCIL_INSTALL_DIR       Override default install directory
  LLM_COUNCIL_NON_INTERACTIVE   Set to true to skip prompts

Default install location: ~/.local/share/llm-council-skill

Examples:
  ./install.sh
  ./install.sh --install-dir ~/my-skills/llm-council
  LLM_COUNCIL_INSTALL_DIR=/opt/llm-council ./install.sh
EOF
        exit 0
        ;;
      *)
        echo "Unknown argument: $1" >&2
        echo "Use --help for usage information." >&2
        exit 1
        ;;
    esac
    shift
  done
}

require_command() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "$1 is required to install LLM Council." >&2
    exit 1
  fi
}

download_command() {
  if command -v curl >/dev/null 2>&1; then
    printf 'curl\n'
    return
  fi

  if command -v wget >/dev/null 2>&1; then
    printf 'wget\n'
    return
  fi

  echo "curl or wget is required to install LLM Council." >&2
  exit 1
}

prompt_yes_no() {
  prompt="$1"

  case "$NON_INTERACTIVE" in
    1 | [Tt][Rr][Uu][Ee] | [Yy][Ee][Ss])
      return 1
      ;;
  esac

  if ( : </dev/tty ) 2>/dev/null; then
    printf '%s [y/N] ' "$prompt" >/dev/tty
    if ! IFS= read -r answer </dev/tty; then
      return 1
    fi
  elif [ -t 0 ]; then
    printf '%s [y/N] ' "$prompt"
    if ! IFS= read -r answer; then
      return 1
    fi
  else
    return 1
  fi

  case "$answer" in
    y | Y | yes | YES)
      return 0
      ;;
    *)
      return 1
      ;;
  esac
}

parse_args "$@"

require_command git
download_cmd="$(download_command)"

step "LLM Council Skill Installer"
echo ""

# Check if directory exists
if [ -d "$INSTALL_DIR" ]; then
  step "Directory exists at $INSTALL_DIR"
  step "Updating to latest version"
  cd "$INSTALL_DIR"
  git pull
else
  step "Installing to $INSTALL_DIR"
  git clone "$REPO_URL" "$INSTALL_DIR"
  cd "$INSTALL_DIR"
fi

echo ""
step "Setting up environment file"
if [ ! -f .env ]; then
  cp .env.example .env
  echo "✓ Created .env file"
  echo ""
  warn "IMPORTANT: You need to add your OpenRouter API key!"
  echo "   Edit $INSTALL_DIR/.env and add:"
  echo "   OPENROUTER_API_KEY=your_key_here"
  echo ""
  echo "   Get a key from: https://openrouter.ai/keys"
  echo ""
  needs_key=1
else
  echo "✓ .env file already exists"
  needs_key=0
fi

echo ""
step "Installing dependencies"
if command -v uv >/dev/null 2>&1; then
  uv sync
  echo "✓ Dependencies installed with uv"
else
  warn "uv not found, using pip"
  python3 -m venv .venv
  # shellcheck disable=SC1091
  . .venv/bin/activate
  pip install -r requirements.txt
  echo "✓ Dependencies installed with pip"
  echo "   Activate with: . $INSTALL_DIR/.venv/bin/activate"
fi

echo ""
step "Installation Complete!"
echo ""

if [ "$needs_key" -eq 1 ]; then
  echo "⚠️  NEXT STEP: Add your API key to .env"
  echo ""
  echo "1. Get your key from: https://openrouter.ai/keys"
  echo "2. Edit $INSTALL_DIR/.env"
  echo "3. Add: OPENROUTER_API_KEY=your_key_here"
  echo ""
fi

echo "Test the installation:"
echo "  cd $INSTALL_DIR"
echo "  uv run python council_run.py 'What is 2+2?' --stages 1"
echo ""
echo "Use from Claude Code:"
echo "  Ask the council: <your question>"
echo "  /llm-council"
echo ""

printf 'LLM Council Skill installed successfully to %s\n' "$INSTALL_DIR"
