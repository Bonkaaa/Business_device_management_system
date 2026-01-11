#!/bin/bash

echo "========================================"
echo "Building DeviceManager Application"
echo "========================================"
echo ""

# Change to project root directory
cd "$(dirname "$0")/.."

# Check if Python is installed
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "ERROR: Python is not installed or not in PATH"
    exit 1
fi

# Use python3 if available, otherwise python
PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    PYTHON_CMD="python"
fi

$PYTHON_CMD --version

echo ""
echo "Installing required packages..."
$PYTHON_CMD -m pip install -r requirement.txt

echo ""
echo "Building executable with PyInstaller..."
$PYTHON_CMD -m PyInstaller --onefile --windowed --name=DeviceManager ./src/main.py

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================"
    echo "Build completed successfully!"
    echo "Executable location: dist/DeviceManager"
    echo "========================================"
else
    echo ""
    echo "ERROR: Build failed!"
    exit 1
fi
