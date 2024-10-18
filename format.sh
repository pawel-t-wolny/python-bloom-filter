#!/bin/bash

# Automatically format Python files with black
poetry run black ./sbloom
# Lint the Python files
poetry run pylint $(git ls-files '*.py')