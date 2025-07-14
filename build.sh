#!/usr/bin/env bash
# Set environment variables to avoid Rust compilation
export SKIP_RUST=1
export CRYPTOGRAPHY_DONT_BUILD_RUST=1

# Install dependencies with --no-build-isolation to avoid Rust
pip install --no-build-isolation -r requirements.txt
