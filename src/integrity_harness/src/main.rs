use std::env;
use std::fs::File;
use std::io::{Read, Error, ErrorKind};
use sha2::{Sha512, Digest};

const HEADER_SIZE: usize = 256;
const MAGIC_NUMBER: u64 = 0x172841544D41;

#[repr(C, packed)]
struct AtmaHeader {
    magic: u64,
    version: u8,
    sequence_id: u64,
    source_offset: u64,
    payload_size: u64,
    payload_hash: [u8; 64], // SHA-512
    iv_nonce: [u8; 12],
    reserved: [u8; 147], // Corrected reserved space to make header 256 bytes
}

impl AtmaHeader {
    fn from_reader<R: Read>(mut reader: R) -> Result<Self, Error> {
        let mut buffer = [0u8; HEADER_SIZE];
        reader.read_exact(&mut buffer)?;
        let header: Self = unsafe { std::mem::transmute(buffer) };

        if u64::from_le(header.magic) != MAGIC_NUMBER {
            return Err(Error::new(ErrorKind::InvalidData, format!("Invalid magic number: got {:#x}", u64::from_le(header.magic))));
        }

        Ok(header)
    }
}

fn verify_file(file_path: &str) -> Result<(), String> {
    let mut file = File::open(file_path).map_err(|e| format!("Failed to open file: {}", e))?;

    let header = AtmaHeader::from_reader(&mut file).map_err(|e| format!("Failed to read or parse header: {}", e))?;

    let mut payload = Vec::new();
    file.read_to_end(&mut payload).map_err(|e| format!("Failed to read payload: {}", e))?;

    if payload.len() as u64 != u64::from_le(header.payload_size) {
        return Err(format!("Payload size mismatch: header says {} bytes, but file has {} bytes", u64::from_le(header.payload_size), payload.len()));
    }

    let mut hasher = Sha512::new();
    hasher.update(&payload);
    let calculated_hash = hasher.finalize();

    if calculated_hash[..] == header.payload_hash[..] {
        Ok(())
    } else {
        Err("Payload hash mismatch: data is corrupt.".to_string())
    }
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        eprintln!("Usage: {} <file.atma>", args[0]);
        std::process::exit(1);
    }

    let file_path = &args[1];
    match verify_file(file_path) {
        Ok(_) => println!("Verification successful: file '{}' is intact.", file_path),
        Err(e) => {
            eprintln!("Verification failed: {}", e);
            std::process::exit(1);
        }
    }
}
