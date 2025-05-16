#!/usr/bin/env bash
export DEBIAN_FRONTEND="noninteractive"
export NEEDRESTART_SUSPEND="1"
set -e

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Install Ollama
if ! command_exists ollama; then
    echo "Ollama not found. Installing..."
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        curl -fsSL https://ollama.com/download/ollama-linux-amd64 -o ollama
        chmod +x ollama
        sudo mv ollama /usr/local/bin/
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install ollama
    else
        echo "Ollama installation not supported on this OS."
    fi
else
    echo "Ollama is already installed."
fi

# Install uv
if ! command_exists uv; then
    echo "uv not found. Installing..."
    curl -Ls https://astral.sh/uv/install.sh | bash
else
    echo "uv is already installed."
fi

# Install Python 3.13
if ! command_exists python3.13; then
    echo "Python 3.13 not found. Installing..."
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt update
        sudo apt install -y software-properties-common
        sudo add-apt-repository ppa:deadsnakes/ppa -y
        sudo apt update
        sudo apt install -y python3.13 python3.13-venv python3.13-distutils
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install python@3.13
    else
        echo "Python 3.13 installation not supported on this OS."
    fi
else
    echo "Python 3.13 is already installed."
fi

echo "Setup complete."