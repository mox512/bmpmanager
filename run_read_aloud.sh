#!/bin/bash

# Activate the virtual environment
cd /home/denis/Documents/CVBuild/
source /home/denis/Documents/CVBuild/venv/bin/activate

# Run the Python script with the selected text
python3 /home/denis/Documents/CVBuild/read_aloud.py "$(xsel)"
sleep 100
exit
