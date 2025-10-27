#!/bin/bash

# Cache pip dependencies
pip install --upgrade pip
pip install --cache-dir .pip-cache -r requirements.txt

