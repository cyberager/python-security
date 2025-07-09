import sys
from datetime import datetime

def banner(msg: str, level: str = "INFO") -> None:
    """
    Affiche un message stylé : [INFO] …, [OK] …, [ERREUR] …, etc.
    """
    levels = {
        "INFO":   "\033[94m[INFO]\033[0m",
        "OK":     "\033[92m[ OK ]\033[0m",
        "ERROR":  "\033[91m[ERREUR]\033[0m",
        "WARN":   "\033[93m[WARN]\033[0m",
    }
    print(f"{levels.get(level,'[----]')} {datetime.now():%H:%M:%S} » {msg}")
    sys.stdout.flush()

def die(msg: str) -> None:
    banner(msg, "ERROR")
    sys.exit(1)
