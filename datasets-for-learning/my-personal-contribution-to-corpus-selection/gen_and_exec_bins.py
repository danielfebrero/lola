import os
import subprocess

def binary_generator():
    i = 0
    while True:
        binary_data = i.to_bytes((i.bit_length() + 7) // 8, 'big') or b'\0'
        yield binary_data
        i += 1

# Chemin du fichier de log
log_file_path = "execution_log.txt"

# Fonction pour écrire les résultats dans le fichier de log
def log_results(filename, stdout, stderr):
    with open(log_file_path, "a") as log_file:
        log_file.write(f"Fichier : {filename}\n")
        log_file.write(f"Sortie : {stdout}\n")
        log_file.write(f"Erreur : {stderr}\n")
        log_file.write("\n")

# Test de la fonction génératrice binaire
bin_gen = binary_generator()

# Générer et tenter d'exécuter les 10 premières séquences binaires
for _ in range(10):
    binary = next(bin_gen)
    filename = f"binary_{_}.bin"
    with open(filename, "wb") as f:
        f.write(binary)
    try:
        os.chmod(filename, 0o755)  # Rendre le fichier exécutable
        result = subprocess.run(f"./{filename}", shell=True, capture_output=True, text=True)
        log_results(filename, result.stdout, result.stderr)
    except Exception as e:
        log_results(filename, "", str(e))
    finally:
        os.remove(filename)  # Nettoyer après l'exécution
