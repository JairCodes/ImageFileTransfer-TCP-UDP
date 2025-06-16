import socket

def start_server(host='0.0.0.0', port=8081, buffer_size=4096):
    # Create TCP socket
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the specified host and port
    server_sock.bind((host, port))
    server_sock.listen(1)
    print(f"[*] Listening on {host}:{port}")

    # Accept a connection from a client
    conn, addr = server_sock.accept()
    print(f"[*] Connection established from {addr}")

    # Receive file data in chunks
    with open('received_input.jpeg', 'wb') as f:
        while True:
            data = conn.recv(buffer_size)
            if not data:
                # No more data received, end of file
                break
            f.write(data)
    print("[*] File received and saved as 'received_input.jpeg'.")

    # Send confirmation back to the client
    confirmation_msg = "SUCCESS: File received"
    conn.sendall(confirmation_msg.encode())
    print("[*] Confirmation sent to client.")

    # Clean up
    conn.close()
    server_sock.close()
    print("[*] Server shutdown.")

if __name__ == '__main__':
    start_server()
