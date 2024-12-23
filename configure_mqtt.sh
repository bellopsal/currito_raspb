#!/bin/bash

# Update and upgrade the system
sudo apt update -y
sudo apt upgrade -y

# Install Mosquitto and Mosquitto clients
sudo apt install -y mosquitto mosquitto-clients

# Copy the mosquitto.conf file to the appropriate directory
sudo cp mosquitto.conf /etc/mosquitto/mosquitto.conf

# Start the Mosquitto service
sudo systemctl start mosquitto.service

# Optional: Enable Mosquitto service to start on boot
sudo systemctl enable mosquitto.service

# Print status of Mosquitto service
sudo systemctl status mosquitto.service
