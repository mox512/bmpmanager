#!/bin/bash

# Activate the virtual environment
source /home/denis/Documents/CVBuild/venv/bin/activate

# Run the Python script with the selected text
python /home/denis/Documents/CVBuild/read_aloud.py "$(xsel | sed -e :a -e 'N;s/\n/ /;ta')"
