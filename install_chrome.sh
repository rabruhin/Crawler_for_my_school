#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Create directories for Chrome and ChromeDriver
mkdir -p /opt/render/project/src/chrome
mkdir -p /opt/render/project/src/chromedriver

# Install Chrome
echo "Installing Chrome..."
wget -q -O google-chrome-stable_current_amd64.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
dpkg-deb -x google-chrome-stable_current_amd64.deb /opt/render/project/src/chrome
rm google-chrome-stable_current_amd64.deb

# Install ChromeDriver
echo "Installing ChromeDriver..."
CHROMEDRIVER_VERSION=$(wget -qO- https://chromedriver.storage.googleapis.com/LATEST_RELEASE)
wget -q -O chromedriver_linux64.zip https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip
unzip chromedriver_linux64.zip -d /opt/render/project/src/chromedriver
rm chromedriver_linux64.zip

echo "Installation completed."
