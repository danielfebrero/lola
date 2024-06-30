import os
import subprocess
import random
import string
import sqlite3

def binary_generator(size=256):
    while True:
        binary_data = os.urandom(size)  # Générer des données binaires aléatoires de taille fixe
        yield binary_data

def random_filename(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length)) + ".bin"

def log_results_to_db(filename, binary_content, stdout, stderr):
    conn = sqlite3.connect('/mnt/data/logs.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO logs (filename, binary_content, stdout, stderr)
        VALUES (?, ?, ?, ?)
    ''', (filename, binary_content, stdout, stderr))
    conn.commit()
    conn.close()

# Ensure the logs table exists
conn = sqlite3.connect('/mnt/data/logs.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY,
        filename TEXT,
        binary_content BLOB,
        stdout TEXT,
        stderr TEXT
    )
''')
conn.commit()
conn.close()

print("Début de la génération et de l'exécution des binaires...")

# Test de la fonction génératrice binaire
bin_gen = binary_generator()

# Boucle infinie pour générer et exécuter des séquences binaires
while True:
    binary = next(bin_gen)
    filename = random_filename()
    with open(filename, "wb") as f:
        f.write(binary)
    try:
        os.chmod(filename, 0o755)  # Rendre le fichier exécutable
        result = subprocess.run(f"./{filename}", shell=True, capture_output=True, text=True)
        log_results_to_db(filename, binary, result.stdout, result.stderr)
        print(f"Exécution de {filename} terminée avec succès.")
    except Exception as e:
        log_results_to_db(filename, binary, "", str(e))
        print(f"Erreur lors de l'exécution de {filename}: {e}")
    finally:
        os.remove(filename)  # Nettoyer après l'exécution

print("Fin de la génération et de l'exécution des binaires.")
