#!/usr/bin/env python3
"""Check if all dependencies are installed."""
import sys
import importlib

REQUIRED = ['grpc', 'transformers', 'torch', 'pydub', 'gradio', 'soundfile']

missing = []
for pkg in REQUIRED:
    try:
        importlib.import_module(pkg)
    except ImportError:
        missing.append(pkg)

if missing:
    print(f"Missing: {', '.join(missing)}")
    sys.exit(1)
print("All dependencies installed")
