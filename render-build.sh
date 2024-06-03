#!/usr/bin/env bash

# Install Google Chrome
echo "Installing Google Chrome"
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
dpkg -x google-chrome-stable_current_amd64.deb /tmp/google-chrome
cp /tmp/google-chrome/opt/google/chrome/chrome /usr/local/bin/

# Install Chromedriver
echo "Installing Chromedriver"
CHROME_DRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE)
wget -N https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip -P /tmp/
unzip /tmp/chromedriver_linux64.zip -d /tmp/
cp /tmp/chromedriver /usr/local/bin/
chmod 0755 /usr/local/bin/chromedriver

# Clean up
rm -rf /tmp/google-chrome
rm /tmp/chromedriver_linux64.zip
