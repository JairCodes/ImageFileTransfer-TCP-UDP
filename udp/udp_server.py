import socket
import argparse
import sys

def start_server(host: str, port: int, buffer_size: int):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.bind((host, port))
        print(f"[*] UDP server listening on {host}:{port}")

        packets = {}
        while True:
            data, addr = sock.recvfrom(buffer_size + 4)
            seq_num = int.from_bytes(data[:4], 'big', signed=True)
            if seq_num == -1:
                print("[*] End-of-transfer marker received.")
                break
            packets[seq_num] = data[4:]

        output_path = 'received_input_udp.jpeg'
        with open(output_path, 'wb') as f:
            for seq in sorted(packets):
                f.write(packets[seq])
        print(f"[*] File received and saved as '{output_path}'.")

        sock.sendto("SUCCESS: File received via UDP".encode(), addr)
        print("[*] Confirmation sent to client.")

    except FileNotFoundError:
        print(f"[ERROR] Could not write file to disk: {output_path}")
    except socket.error as e:
        print(f"[ERROR] Socket error: {e}")
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
    finally:
        sock.close()
        print("[*] UDP server shutdown.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='UDP Image File Transfer Server')
    parser.add_argument('--host', default='0.0.0.0', help='IP address to bind')
    parser.add_argument('--port', type=int, default=8080, help='Port to bind')
    parser.add_argument('--buffer', type=int, dest='buffer_size', default=4096, help='Payload buffer size')
    args = parser.parse_args()

    try:
        start_server(args.host, args.port, args.buffer_size)
    except KeyboardInterrupt:
        print('\n Shutdown requested by user.')
        sys.exit(0)
