#!/usr/bin/env bash

# Install Google Chrome
echo "Installing Google Chrome"
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
mkdir -p /usr/local/bin/chrome
dpkg -x google-chrome-stable_current_amd64.deb /usr/local/bin/chrome
chmod +x /usr/local/bin/chrome/opt/google/chrome/chrome

# Install Chromedriver
echo "Installing Chromedriver"
CHROME_DRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE)
wget -N https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip -P /tmp/
unzip /tmp/chromedriver_linux64.zip -d /tmp/
mv /tmp/chromedriver /usr/local/bin/
chmod +x /usr/local/bin/chromedriver

# Update PATH environment variable


# Clean up
rm google-chrome-stable_current_amd64.deb
rm /tmp/chromedriver_linux64.zip
