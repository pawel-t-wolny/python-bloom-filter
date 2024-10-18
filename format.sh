#!/bin/bash

# Automatically format Python files with black
black ./src
# Lint the Python files
find ./src -name "*.py" | xargs pylint