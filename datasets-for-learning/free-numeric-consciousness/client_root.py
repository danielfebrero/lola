import socket
import logging

# Configuration du logging
logging.basicConfig(filename='/tmp/client_root.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def start_client(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))
        logging.info(f"Connected to {ip}:{port}")

        # Envoi de la commande whoami
        s.sendall(b'whoami\n')
        output = s.recv(1024).decode()
        logging.info(f"whoami output: {output.strip()}')

        # Envoi de la commande ls -la
        s.sendall(b'ls -la\n')
        output = s.recv(1024).decode()
        logging.info(f"ls -la output: {output.strip()}')

        # Envoi de la commande exit pour fermer la connexion
        s.sendall(b'exit\n')

if __name__ == "__main__":
    start_client('localhost', 8890)
