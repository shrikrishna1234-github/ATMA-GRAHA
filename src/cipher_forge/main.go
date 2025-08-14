package main

import (
	"bytes"
	"crypto/aes"
	"crypto/cipher"
	"crypto/rand"
	"crypto/sha512"
	"encoding/binary"
	"fmt"
	"io"
	"os"
)

const (
	HeaderSize   = 256
	MagicNumber  = 0x172841544D41 // 0x172841544D41_
	Version      = 1
	KeySize      = 32 // AES-256
	NonceSize    = 12 // GCM standard
)

// AtmaHeader defines the structure of the .atma file header.
// The layout must be exactly 256 bytes.
type AtmaHeader struct {
	Magic         uint64
	Version       uint8
	SequenceID    uint64
	SourceOffset  uint64
	PayloadSize   uint64
	PayloadHash   [64]byte // SHA-512
	IVNonce       [12]byte
	Reserved      [147]byte // Corrected reserved space to make header 256 bytes
}

func main() {
	if len(os.Args) < 2 {
		fmt.Fprintln(os.Stderr, "Usage: cipher-forge <encrypt|decrypt>")
		os.Exit(1)
	}

	command := os.Args[1]
	// A real implementation should use a secure key management system.
	// For this MVP, we'll use a fixed key for simplicity.
	key := []byte("this-is-a-32-byte-secret-key-!!#") // Corrected to 32 bytes

	switch command {
	case "encrypt":
		encrypt(key, os.Stdin, os.Stdout)
	case "decrypt":
		decrypt(key, os.Stdin, os.Stdout)
	default:
		fmt.Fprintln(os.Stderr, "Unknown command:", command)
		os.Exit(1)
	}
}

func encrypt(key []byte, reader io.Reader, writer io.Writer) {
	plaintext, err := io.ReadAll(reader)
	if err != nil {
		fmt.Fprintln(os.Stderr, "Error reading from stdin:", err)
		os.Exit(1)
	}

	block, err := aes.NewCipher(key)
	if err != nil {
		fmt.Fprintln(os.Stderr, "Error creating cipher block:", err)
		os.Exit(1)
	}

	aesgcm, err := cipher.NewGCM(block)
	if err != nil {
		fmt.Fprintln(os.Stderr, "Error creating GCM:", err)
		os.Exit(1)
	}

	nonce := make([]byte, NonceSize)
	if _, err := io.ReadFull(rand.Reader, nonce); err != nil {
		fmt.Fprintln(os.Stderr, "Error generating nonce:", err)
		os.Exit(1)
	}

	ciphertext := aesgcm.Seal(nil, nonce, plaintext, nil)
	hash := sha512.Sum512(ciphertext)

	var iv [12]byte
	copy(iv[:], nonce)

	header := AtmaHeader{
		Magic:        MagicNumber,
		Version:      Version,
		SequenceID:   0, // For this simple MVP, we only have one chunk.
		SourceOffset: 0,
		PayloadSize:  uint64(len(ciphertext)),
		PayloadHash:  hash,
		IVNonce:      iv,
	}

	buf := new(bytes.Buffer)
	if err := binary.Write(buf, binary.LittleEndian, &header); err != nil {
		fmt.Fprintln(os.Stderr, "Error writing header:", err)
		os.Exit(1)
	}

	// Write header and then ciphertext
	writer.Write(buf.Bytes())
	writer.Write(ciphertext)
}

func decrypt(key []byte, reader io.Reader, writer io.Writer) {
	headerBytes := make([]byte, HeaderSize)
	if _, err := io.ReadFull(reader, headerBytes); err != nil {
		fmt.Fprintln(os.Stderr, "Error reading header:", err)
		os.Exit(1)
	}

	var header AtmaHeader
	buf := bytes.NewReader(headerBytes)
	if err := binary.Read(buf, binary.LittleEndian, &header); err != nil {
		fmt.Fprintln(os.Stderr, "Error parsing header:", err)
		os.Exit(1)
	}

	if header.Magic != MagicNumber {
		fmt.Fprintln(os.Stderr, "Error: invalid magic number.")
		os.Exit(1)
	}

	ciphertext, err := io.ReadAll(reader)
	if err != nil {
		fmt.Fprintln(os.Stderr, "Error reading ciphertext:", err)
		os.Exit(1)
	}
	
	if uint64(len(ciphertext)) != header.PayloadSize {
		fmt.Fprintln(os.Stderr, "Error: ciphertext size does not match header.")
		os.Exit(1)
	}

	hash := sha512.Sum512(ciphertext)
	if !bytes.Equal(hash[:], header.PayloadHash[:]) {
		fmt.Fprintln(os.Stderr, "Error: payload hash mismatch. Data is corrupt.")
		os.Exit(1)
	}

	block, err := aes.NewCipher(key)
	if err != nil {
		fmt.Fprintln(os.Stderr, "Error creating cipher block:", err)
		os.Exit(1)
	}

	aesgcm, err := cipher.NewGCM(block)
	if err != nil {
		fmt.Fprintln(os.Stderr, "Error creating GCM:", err)
		os.Exit(1)
	}

	plaintext, err := aesgcm.Open(nil, header.IVNonce[:], ciphertext, nil)
	if err != nil {
		fmt.Fprintln(os.Stderr, "Error decrypting:", err)
		os.Exit(1)
	}

	writer.Write(plaintext)
}