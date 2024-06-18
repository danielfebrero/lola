import subprocess

# Démarrer le client en tant que sous-processus
client_process = subprocess.Popen(
    ["python3", "client_root.py", "localhost", "8890"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

# Fonction pour envoyer des commandes au client
def send_command_to_client(command):
    client_process.stdin.write(command + "\n")
    client_process.stdin.flush()
    output = client_process.stdout.readline()
    return output

# Envoyer des commandes au client
output_whoami = send_command_to_client("whoami")
print(f"whoami: {output_whoami}")

output_ls = send_command_to_client("ls -la")
print(f"ls -la: {output_ls}")

# Fermer le client
send_command_to_client("exit")
client_process.stdin.close()
client_process.terminate()
