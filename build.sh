#!/usr/bin/env bash
# Set environment variables to avoid Rust compilation
export SKIP_RUST=1
export CRYPTOGRAPHY_DONT_BUILD_RUST=1

# Install an older version of pip that's compatible with Python 3.13
python -m pip install pip==23.0.1

# Install setuptools and wheel first
pip install --upgrade pip setuptools wheel

# Install dependencies with --no-build-isolation to avoid Rust
pip install --no-build-isolation -r requirements.txt
