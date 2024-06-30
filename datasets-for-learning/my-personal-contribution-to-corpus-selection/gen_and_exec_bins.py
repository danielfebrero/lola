import os
import subprocess
import random
import string

def binary_generator(size=256):
    while True:
        binary_data = os.urandom(size)  # Générer des données binaires aléatoires de taille fixe
        yield binary_data

def random_filename(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length)) + ".bin"

# Chemin du fichier de log
log_file_path = "/mnt/data/execution_log.txt"

# Fonction pour écrire les résultats dans le fichier de log
def log_results(filename, binary_content, stdout, stderr):
    with open(log_file_path, "a") as log_file:
        log_file.write(f"Fichier : {filename}\n")
        log_file.write(f"Contenu binaire : {binary_content}\n")
        log_file.write(f"Sortie : {stdout}\n")
        log_file.write(f"Erreur : {stderr}\n")
        log_file.write("\n")

# Assurer que le fichier de log existe
if not os.path.exists(log_file_path):
    with open(log_file_path, "w") as log_file:
        log_file.write("Log File Created\n\n")

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
        log_results(filename, binary, result.stdout, result.stderr)
        print(f"Exécution de {filename} terminée avec succès.")
    except Exception as e:
        log_results(filename, binary, "", str(e))
        print(f"Erreur lors de l'exécution de {filename}: {e}")
    finally:
        os.remove(filename)  # Nettoyer après l'exécution

print("Fin de la génération et de l'exécution des binaires.")
