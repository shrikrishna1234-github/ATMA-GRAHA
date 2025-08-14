<div align="center">
  <img src="https://images.unsplash.com/photo-1555949963-ff9fe0c870eb?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80" alt="ATMA-GRAHA Header Image" width="700"/>

  # 🔹 ATMA-GRAHA 🔹

  ### Pure reality preservation.
</div>

<div align="center">

[![C++](https://img.shields.io/badge/C++-00599C?style=for-the-badge&logo=cplusplus&logoColor=white)](https://isocpp.org/) 
[![Go](https://img.shields.io/badge/Go-00ADD8?style=for-the-badge&logo=go&logoColor=white)](https://golang.org/) 
[![Rust](https://img.shields.io/badge/Rust-000000?style=for-the-badge&logo=rust&logoColor=white)](https://www.rust-lang.org/) 
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/) 
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

</div>

---

## Core Concept

**ATMA-GRAHA** is a **forensically perfect, bit-for-bit** disk capture and restoration system. It is built around an unbreakable, encrypted `.atma` file format designed for pure, lossless reality preservation. No compression, no approximations—just a perfect digital reflection of the source media.

**⚠️ Important Note:** This project is currently a **Minimum Viable Product (MVP)**. It demonstrates the core functionality and architectural principles but is not yet a production-ready tool. It is intended for educational and experimental purposes.

This project is an experiment in polyglot programming, leveraging the strengths of multiple languages to create a single, cohesive tool.

## The Polyglot Trinity

Each language was chosen for its optimal role in the pipeline:

*   **C++ (Yama-Yantra):** Powers the high-speed, raw disk I/O engine. It reads and writes raw byte streams from the source or to the destination with maximum performance.
*   **Go (Cipher-Forge):** Handles the high-concurrency cryptography. It encrypts and decrypts data streams using AES-256-GCM and verifies SHA-512 hashes in a parallel, efficient manner.
*   **Rust (Integrity Harness):** Provides memory-safe, high-reliability verification. It parses the `.atma` file format and validates its integrity, ensuring that the archive is sound.
*   **Python (Brahma-Sutra):** Orchestrates the entire process. The user-friendly CLI is the master conductor, weaving the other components together into a seamless workflow.

## How It Works

The process is a clean, linear pipeline designed for speed and reliability.

#### Capture
```
[Source Disk] ➡️ [C++ Engine] ➡️ [Go Encryptor] ➡️ [.atma File]
```

#### Restore
```
[.atma File] ➡️ [Go Decryptor] ➡️ [C++ Engine] ➡️ [Destination Disk]
```

## Key Features

*   **Lossless:** Creates a perfect 1:1 copy of the source data.
*   **Secure:** All data is encrypted with AES-256-GCM, and integrity is verified with SHA-512.
*   **Fast:** The pipeline is designed for high-throughput, with minimal CPU waste.
*   **Verifiable:** The Rust-powered `verify` command ensures your archives are always sound.

## Getting Started

### Prerequisites

You must have the following compiler toolchains installed and available in your PATH:
*   `g++` (for C++)
*   `go` (for Go)
*   `cargo` (for Rust)

### Build

*   **On Windows:**
    ```cmd
    build.bat
    ```
*   **On Linux / macOS:**
    ```bash
    chmod +x build.sh
    ./build.sh
    ```

### Usage

The CLI provides three simple commands:

1.  **Capture a file:**
    ```bash
    python bin/atmagraha capture <source_file> <destination.atma>
    ```

2.  **Restore a file:**
    ```bash
    python bin/atmagraha restore <source.atma> <destination_file>
    ```

3.  **Verify a file's integrity:**
    ```bash
    python bin/atmagraha verify <source.atma>
    ```

## The `.atma` File Format

The `.atma` format consists of a 256-byte header followed by the encrypted payload.

| Field          | Size (bytes) | Description                               |
|----------------|--------------|-------------------------------------------|
| Magic Number   | 8            | `0x172841544D41_`                         |
| Version        | 1            | Format version (currently 1)              |
| Sequence ID    | 8            | Chunk index for multi-file archives       |
| Source Offset  | 8            | Byte offset in the original source        |
| Payload Size   | 8            | Exact length of the encrypted payload     |
| SHA-512 Hash   | 64           | Hash of the encrypted payload for integrity |
| IV / Nonce     | 12           | Unique nonce for AES-GCM encryption       |
| Reserved       | 147          | For future use                            |

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

## License

Distributed under the MIT License. See `LICENSE` for more information.