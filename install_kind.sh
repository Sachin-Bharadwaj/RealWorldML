#!/bin/bash

# Create a directory for kind
mkdir -p ~/bin

# Download kind binary
curl -Lo ~/bin/kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-amd64

# Make kind executable
chmod +x ~/bin/kind

# Add ~/bin to PATH if it's not already there
if ! grep -q 'export PATH="$HOME/bin:$PATH"' ~/.bashrc; then
    echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
    echo "Added ~/bin to PATH in .bashrc"
fi

# Source .bashrc to update PATH in current session
source ~/.bashrc

echo "kind has been installed and added to PATH"
echo "You can verify the installation by running: kind version" 