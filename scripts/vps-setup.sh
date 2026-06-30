#!/bin/bash
# EXL-CRM VPS Setup Script
set -e

echo "=== EXL-CRM VPS Setup ==="

# Update system
echo "1. Updating system..."
apt update && apt upgrade -y

# Install Docker
echo "2. Installing Docker..."
curl -fsSL https://get.docker.com | sh

# Install Docker Compose
echo "3. Installing Docker Compose..."
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Add current user to docker group
echo "4. Configuring Docker permissions..."
usermod -aG docker $USER

# Verify installations
echo ""
echo "=== Installation Complete ==="
docker --version
docker-compose --version

echo ""
echo "Run 'exit' then reconnect via SSH to apply docker group changes, or run:"
echo "  su - $USER"
echo ""
echo "Then clone the repo:"
echo "  cd /var/www"
echo "  git clone https://github.com/rubeshgithub/exlcrm.git"
echo "  cd exlcrm && cp backend/.env.example backend/.env"