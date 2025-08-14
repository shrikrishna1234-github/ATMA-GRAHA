#!/bin/bash
# Exit if any command fails
set -e

echo "Building C++ Yama-Engine..."
g++ -o bin/yama-engine src/core_engine/main.cpp -std=c++17

echo "Building Go Cipher-Forge..."
go build -o bin/cipher-forge src/cipher_forge/main.go

echo "Building Rust Integrity-Harness..."
(cd src/integrity_harness && cargo build --release)
cp src/integrity_harness/target/release/integrity-harness bin/

echo "Build complete. Binaries are in the 'bin' directory."