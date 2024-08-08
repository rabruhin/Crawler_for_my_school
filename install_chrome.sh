#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Install Chrome
echo "Installing Chrome..."
wget -q -O google-chrome-stable_current_amd64.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt-get update && apt-get install -y ./google-chrome-stable_current_amd64.deb
rm google-chrome-stable_current_amd64.deb

echo "Installation completed."
