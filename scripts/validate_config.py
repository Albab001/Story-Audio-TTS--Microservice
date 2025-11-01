#!/usr/bin/env python3
"""Validate configuration settings."""
import sys
from config import Config

if not Config.validate():
    print("Configuration validation failed!")
    sys.exit(1)
print("Configuration valid")
