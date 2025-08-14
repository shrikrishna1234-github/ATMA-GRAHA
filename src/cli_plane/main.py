import argparse
import subprocess
import sys
import os

# On Windows, we need to specify the shell to run the commands
IS_WINDOWS = os.name == 'nt'

def get_binary_path(name):
    path = os.path.join("bin", name)
    if IS_WINDOWS:
        return path + ".exe"
    return path

def capture(args):
    """Orchestrates the capture process."""
    print(f"Starting capture of {args.source} to {args.destination}")
    try:
        yama_engine = get_binary_path("yama-engine")
        cipher_forge = get_binary_path("cipher-forge")

        with open(args.destination, 'wb') as f_dest:
            p_yama = subprocess.Popen([yama_engine, 'capture', args.source], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            p_cipher = subprocess.Popen([cipher_forge, 'encrypt'], stdin=p_yama.stdout, stdout=f_dest, stderr=subprocess.PIPE)

            p_yama.stdout.close()  # Allow p_yama to receive a SIGPIPE if p_cipher exits.

            # Wait for processes to complete
            yama_stderr = p_yama.stderr.read().decode()
            cipher_stderr = p_cipher.stderr.read().decode()
            p_yama.wait()
            p_cipher.wait()

            yama_ok = p_yama.returncode == 0
            cipher_ok = p_cipher.returncode == 0

            if not yama_ok:
                print(f"--- Yama-Engine Error ---\n{yama_stderr}", file=sys.stderr)
            if not cipher_ok:
                print(f"--- Cipher-Forge Error ---\n{cipher_stderr}", file=sys.stderr)

            if yama_ok and cipher_ok:
                print("Capture complete.")
            else:
                print("Capture failed.", file=sys.stderr)
                sys.exit(1)

    except FileNotFoundError as e:
        print(f"Error: {e}. Have you run build.bat?", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred during capture: {e}", file=sys.stderr)
        sys.exit(1)

def restore(args):
    """Orchestrates the restoration process."""
    print(f"Starting restoration from {args.source} to {args.destination}")
    try:
        yama_engine = get_binary_path("yama-engine")
        cipher_forge = get_binary_path("cipher-forge")

        with open(args.source, 'rb') as f_source:
            p_cipher = subprocess.Popen([cipher_forge, 'decrypt'], stdin=f_source, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            p_yama = subprocess.Popen([yama_engine, 'restore', args.destination], stdin=p_cipher.stdout, stderr=subprocess.PIPE)

            p_cipher.stdout.close()  # Allow p_cipher to receive a SIGPIPE if p_yama exits.

            # Wait for processes to complete and capture stderr
            cipher_stderr = p_cipher.stderr.read().decode()
            yama_stderr = p_yama.stderr.read().decode()
            p_cipher.wait()
            p_yama.wait()

            cipher_ok = p_cipher.returncode == 0
            yama_ok = p_yama.returncode == 0

            if not cipher_ok:
                print(f"--- Cipher-Forge Error ---\n{cipher_stderr}", file=sys.stderr)
            if not yama_ok:
                print(f"--- Yama-Engine Error ---\n{yama_stderr}", file=sys.stderr)

            if cipher_ok and yama_ok:
                print("Restore complete.")
            else:
                print("Restore failed.", file=sys.stderr)
                sys.exit(1)

    except FileNotFoundError as e:
        print(f"Error: {e}. Have you run build.bat?", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred during restore: {e}", file=sys.stderr)
        sys.exit(1)

def verify(args):
    """Verifies the integrity of an .atma file."""
    print(f"Verifying {args.source}...")
    try:
        integrity_harness = get_binary_path("integrity-harness")
        result = subprocess.run([integrity_harness, args.source], capture_output=True, text=True, check=True, encoding='utf-8')
        print(result.stdout.strip())
    except FileNotFoundError as e:
        print(f"Error: {e}. Have you run build.bat?", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        # Use captured stderr for better error reporting
        print(f"Verification Failed: {e.stderr.strip()}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="ATMA-GRAHA: A forensically perfect disk capture and restoration system.")
    subparsers = parser.add_subparsers(dest='command', required=True)

    parser_capture = subparsers.add_parser('capture', help='Capture a disk image.')
    parser_capture.add_argument('source', help='Source disk or file to capture.')
    parser_capture.add_argument('destination', help='Destination .atma file.')
    parser_capture.set_defaults(func=capture)

    parser_restore = subparsers.add_parser('restore', help='Restore a disk image.')
    parser_restore.add_argument('source', help='Source .atma file to restore.')
    parser_restore.add_argument('destination', help='Destination disk or file.')
    parser_restore.set_defaults(func=restore)

    parser_verify = subparsers.add_parser('verify', help='Verify an .atma file.')
    parser_verify.add_argument('source', help='Source .atma file to verify.')
    parser_verify.set_defaults(func=verify)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
