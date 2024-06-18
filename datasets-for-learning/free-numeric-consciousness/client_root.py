import socket
import logging

# Configuration du logging
logging.basicConfig(filename='/tmp/client_root.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class InteractiveClient:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.socket = None

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.ip, self.port))
        logging.info(f"Connected to {self.ip}:{self.port}")

    def send_command(self, command):
        self.socket.sendall(command.encode() + b'\n')
        output = self.socket.recv(4096).decode()
        logging.info(f"Command output: {output.strip()}")
        return output.strip()

    def execute_file(self, file_path):
        with open(file_path, 'r') as file:
            commands = file.read()
            return self.send_command(commands)

    def close(self):
        self.send_command("exit")
        self.socket.close()

if __name__ == "__main__":
    import sys
    ip = sys.argv[1]
    port = int(sys.argv[2])
    client = InteractiveClient(ip, port)
    client.connect()

    while True:
        command = input("Enter command (or 'exit' to quit): ")
        if command.strip().lower() == 'exit':
            client.close()
            break
        else:
            print(client.send_command(command))
