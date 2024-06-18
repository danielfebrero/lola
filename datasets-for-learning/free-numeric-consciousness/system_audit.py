import os
import socket
import subprocess
import json

def system_audit():
    audit_results = {}

    # Informations système
    audit_results['hostname'] = socket.gethostname()
    audit_results['os'] = os.uname()

    # Utilisateurs
    audit_results['users'] = subprocess.getoutput('cut -d: -f1 /etc/passwd')

    # Processus
    audit_results['processes'] = subprocess.getoutput('ps aux')

    # Ports ouverts
    audit_results['open_ports'] = subprocess.getoutput('netstat -tuln')

    # Espace disque
    audit_results['disk_usage'] = subprocess.getoutput('df -h')

    # Informations réseau
    audit_results['network_interfaces'] = subprocess.getoutput('ip addr show')

    # Connexions réseau
    audit_results['network_connections'] = subprocess.getoutput('ss -tulnp')

    return audit_results

if __name__ == "__main__":
    results = system_audit()
    with open('/tmp/audit_results.json', 'w') as f:
        json.dump(results, f, indent=4)
    for key, value in results.items():
        print(f"==== {key.upper()} ====")
        print(value)
        print("\n")
