#!/bin/bash

# Location Finder 2.0 - Kali Linux Auto-Setup Script
# --------------------------------------------------

# Text colors
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}Starting Kali Linux Setup for Location Finder 2.0...${NC}"

# Check for Python
if ! command -v python3 &> /dev/null
then
    echo -e "${RED}Python3 not found. Installing...${NC}"
    sudo apt update && sudo apt install -y python3 python3-pip
fi

# Install Dependencies
echo -e "${CYAN}Installing Python dependencies...${NC}"
pip3 install flask pyngrok colorama user-agents flask-cors requests --break-system-packages

# Create directory structure
echo -e "${CYAN}Preparing directory structure...${NC}"
mkdir -p logs

# Ngrok Instructions
echo -e "\n${YELLOW}--------------------------------------------------${NC}"
echo -e "${GREEN}SETUP COMPLETE!${NC}"
echo -e "${YELLOW}--------------------------------------------------${NC}"
echo -e "${NC}Remaining steps:"
echo -e "1. Get your Ngrok Authtoken from: ${CYAN}https://dashboard.ngrok.com/get-started/your-authtoken${NC}"
echo -e "2. Configure it with: ${GREEN}ngrok config add-authtoken <your_token>${NC}"
echo -e "3. Launch the tool with: ${GREEN}python3 kali_tool.py${NC}"
echo -e "${YELLOW}--------------------------------------------------${NC}\n"
