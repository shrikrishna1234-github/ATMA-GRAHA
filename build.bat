@echo off
setlocal

REM Exit if any command fails
set CXX=g++
set GO=go
set CARGO=cargo

echo Building C++ Yama-Engine...
%CXX% -o bin\yama-engine.exe src\core_engine\main.cpp -std=c++17
if errorlevel 1 (
    echo Failed to build Yama-Engine.
    exit /b 1
)

echo Building Go Cipher-Forge...
%GO% build -o bin\cipher-forge.exe src\cipher_forge\main.go
if errorlevel 1 (
    echo Failed to build Cipher-Forge.
    exit /b 1
)

echo Building Rust Integrity-Harness...
cd src\integrity_harness
%CARGO% build --release
if errorlevel 1 (
    echo Failed to build Integrity-Harness.
    cd ..\..
    exit /b 1
)
cd ..\..

REM Copy the Rust binary to the bin directory
copy src\integrity_harness\target\release\integrity-harness.exe bin\integrity-harness.exe

echo Build complete. Binaries are in the 'bin' directory.
