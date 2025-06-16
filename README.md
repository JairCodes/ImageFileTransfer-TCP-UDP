# Image File Transfer Using TCP & UDP Socket Programming

## Project Overview
This project consists of two Python scripts—one for TCP and one for UDP—that demonstrate reliable (TCP) and connectionless (UDP) image file transfers using socket programming. A sample JPEG (`input.jpeg`) is sent from a client to a server over each transport protocol, and end-to-end performance metrics (file size, chunk/packet count, transfer time, throughput) are recorded for comparison, showcasing hands-on experience in scripting network applications.

## Prerequisites
- Python 3.6 or later
- No external libraries required (uses Python standard library)

## Usage
Run each client and server in separate terminals. Use the `--host`, `--port`, `--file`, and `--buffer` flags to customize behavior.

### TCP Transfer
1. **Start the TCP server**
   ```bash
   cd tcp
   python tcp_server.py
2. **Run the TCP client**
   ```bash
   cd tcp
   python tcp_client.py --host 127.0.0.1 --port 8081 --file input.jpeg --buffer 4096

### UDP Transfer
1. **Start the UDP server**
   ```bash
   cd udp
   python udp_server.py
2. **Run the UDP client**
   ```bash
   cd udp
   python udp_client.py --host 127.0.0.1 --port 8080 --file input.jpeg --buffer 4096
