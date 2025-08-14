# ATMA-GRAHA — MVP DESCRIPTION

## 🔹 Core Concept
A **forensically perfect, bit-for-bit** disk capture and restoration system built around an unbreakable, encrypted `.atma` file format.  
No compression, no data loss — **pure reality preservation**.  
It operates as a **polyglot trinity**:
1. **C++ (Yama-Yantra)** — High-speed raw disk I/O.
2. **Go (Cipher-Forge)** — Parallel AES-256-GCM encryption + SHA-512 hashing.
3. **Rust (Integrity Harness)** — Verification, safety, and `.atma` parsing.
4. **Python (Brahma-Sutra)** — CLI orchestration & user interface.

---

## 🔹 MVP Flow
**Capture:**
`READ raw block → ENCRYPT → HASH → WRITE to .atma`  
- 1:1 disk size match (e.g., 2TB disk → 2TB total `.atma` files).
- `.atma` header stores metadata (magic, version, sequence, source offset, payload size, hash, IV).
- Fast IPC pipeline: `C++ → Go → C++`, orchestrated by Python.

**Restore:**
Reverse process with verification via Rust.

---

## 🔹 .atma File Structure
**256-byte header + Encrypted Payload**
- **Magic**: `0x172841544D41_`  
- **Version**: 1  
- **Sequence ID**: chunk index  
- **Source Offset**: original byte offset  
- **Payload Size**: exact encrypted block length  
- **SHA-512 Payload Hash**: integrity check  
- **IV Nonce**: 12 bytes per chunk  
- Reserved space for future use.

---

## 🔹 File Structure (MVP Minimal Form)
```

ATMA-GRAHA/
├── README.md
├── build.sh
├── bin/
│   ├── atmagraha        # Python CLI
│   ├── yama-engine      # C++ I/O engine
│   └── cipher-forge     # Go crypto daemon
├── src/
│   ├── core\_engine/     # C++ disk I/O + IPC
│   ├── cli\_plane/       # Python CLI & orchestration
│   ├── integrity\_harness/ # Rust verification
│   └── cipher\_forge/    # Go encryption workers
└── tests/               # Basic integration/unit tests

```

---

## 🔹 Why This MVP is Ready
- **Lossless**: No compression, 100% accurate restoration.
- **Blazing Fast**: No CPU waste on approximations; raw I/O + crypto only.
- **Cross-Verified**: Rust enforces format & integrity.
- **Polyglot Power**: Each language chosen for its optimal domain role.
- **Minimal Yet Complete**: Can capture, encrypt, verify, and restore immediately.
