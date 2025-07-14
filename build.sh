#!/usr/bin/env bash

# --- Upgrade pip, setuptools, and wheel to avoid pkgutil.ImpImporter error ---
python -m pip install --upgrade pip setuptools wheel

# --- Optional: skip Rust builds for cryptography-related packages ---
export SKIP_RUST=1
export CRYPTOGRAPHY_DONT_BUILD_RUST=1

# --- Install dependencies without build isolation (avoids rust/toolchain issues) ---
pip install --no-build-isolation -r requirements.txt
