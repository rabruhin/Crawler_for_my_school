#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Install Chrome
echo "Installing Chrome..."
wget -q -O google-chrome-stable_current_amd64.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
mkdir -p /tmp/chrome
dpkg-deb -x google-chrome-stable_current_amd64.deb /tmp/chrome
rm google-chrome-stable_current_amd64.deb
mv /tmp/chrome/opt/google/chrome /opt/chrome

# Install ChromeDriver
echo "Installing ChromeDriver..."
CHROMEDRIVER_VERSION=$(wget -qO- https://chromedriver.storage.googleapis.com/LATEST_RELEASE)
wget -q -O chromedriver_linux64.zip https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip
unzip chromedriver_linux64.zip -d /opt/chrome/
rm chromedriver_linux64.zip

echo "Installation completed."
