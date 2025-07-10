#!/bin/bash
# Cleanup script for Story2Audio Microservice

echo "Cleaning up Story2Audio project..."

# Remove Python cache files
echo "Removing Python cache files..."
find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete
find . -type f -name "*.pyo" -delete
find . -type f -name "*.pyd" -delete

# Remove temporary files
echo "Removing temporary files..."
rm -rf .pytest_cache
rm -rf .mypy_cache
rm -rf .coverage
rm -rf htmlcov
rm -rf dist
rm -rf build
rm -rf *.egg-info

# Remove output files (optional - comment out if you want to keep outputs)
# echo "Removing output files..."
# rm -rf outputs/temp/*
# rm -rf outputs/final/*

# Remove logs
echo "Removing log files..."
find . -type f -name "*.log" -delete

echo "Cleanup complete!"
