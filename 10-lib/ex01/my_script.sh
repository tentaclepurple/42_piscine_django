#!/bin/bash

LIB_FOLDER="local_lib"
LOG_FILE="installation.log"

# Display the pip version
echo "Using pip version:"

pip --version

# Remove existing local_lib directory if it exists
if [ -d "$LIB_FOLDER" ]; then
    echo "Removing existing $LIB_FOLDER directory..."
    rm -rf "$LIB_FOLDER"
fi

pip install git+https://github.com/jaraco/path.git --target="$LIB_FOLDER" > "$LOG_FILE" 2>&1



# Check if the installation was successful
if [ $? -eq 0 ]; then
    echo "path.py has been successfully installed."
    echo "Executing my_program.py..."
    python3 my_program.py
else
    echo "Failed to install path.py."
fi
