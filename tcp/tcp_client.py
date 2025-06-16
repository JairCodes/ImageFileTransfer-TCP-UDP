import socket
import argparse
import sys
import time
import os

def send_file(host: str, port: int, filename: str, buffer_size: int):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # File size metric
        file_size = os.path.getsize(filename)
        print(f"[*] Preparing to send '{filename}' ({file_size} bytes) to {host}:{port}")
        print(f"[*] Using buffer size of {buffer_size} bytes")

        # Start timer
        start_time = time.time()

        # Connect to the server
        sock.connect((host, port))
        print(f"[*] Connected to {host}:{port}")

        # Send the file in chunks
        seq = 0
        with open(filename, 'rb') as f:
            while True:
                chunk = f.read(buffer_size)
                if not chunk:
                    break
                sock.sendall(chunk)
                seq += 1
        print(f"[*] File '{filename}' sent ({seq} chunks).")

        # Signal end-of-file
        sock.shutdown(socket.SHUT_WR)

        # Wait for server confirmation
        confirmation = sock.recv(buffer_size).decode()
        end_time = time.time()
        print(f"[*] Server response: {confirmation}")

        # Compute metrics
        duration = end_time - start_time
        throughput_mbps = (file_size * 8) / (duration * 1_000_000)

        # Summary
        print("\n=== TCP Transfer Summary ===")
        print(f"File size     : {file_size} bytes")
        print(f"Buffer size   : {buffer_size} bytes")
        print(f"Chunks sent   : {seq}")
        print(f"Total time    : {duration:.3f} s")
        print(f"Throughput    : {throughput_mbps:.2f} Mbps")

    except FileNotFoundError:
        print(f"[ERROR] File not found: {filename}")
    except socket.error as e:
        print(f"[ERROR] Socket error: {e}")
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
    finally:
        sock.close()
        print("[*] Connection closed.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='TCP Image File Transfer Client with Metrics')
    parser.add_argument('--host', default='127.0.0.1', help='Server IP address')
    parser.add_argument('--port', type=int, default=8081, help='Server port number')
    parser.add_argument('--file', dest='filename', default='input.jpeg', help='File to send')
    parser.add_argument('--buffer', type=int, dest='buffer_size', default=4096, help='Chunk size in bytes')
    args = parser.parse_args()

    try:
        send_file(args.host, args.port, args.filename, args.buffer_size)
    except KeyboardInterrupt:
        print("\n[INFO] Shutdown requested by user.")
        sys.exit(0)