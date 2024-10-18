#!/bin/bash

# Automatically format Python files with black
black ./sbloom
# Lint the Python files
find ./sbloom "*.py" | xargs pylint