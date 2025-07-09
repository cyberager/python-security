"""
dvwa.py – connexion et maintien de session DVWA
"""
import requests
from bs4 import BeautifulSoup
from utils import banner
import config

# Session HTTP globale (cookies, headers partagés)
session = requests.Session()

def _extract_token(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    tok = soup.find("input", {"name": "user_token"})
    return tok["value"] if tok else ""

def login() -> bool:
    login_url = f"http://{config.TARGET_IP}:{config.TARGET_PORT}/dvwa/login.php"
    banner("Ouverture de session DVWA")

    try:
        # 1) GET pour récupérer le token
        r = session.get(login_url, timeout=5)
        token = _extract_token(r.text)

        # 2) POST d’authentification
        payload = {
            "username":   config.DVWA_USER,
            "password":   config.DVWA_PASS,
            "Login":      "Login",
            "user_token": token
        }
        r = session.post(login_url, data=payload, timeout=5, allow_redirects=True)
        if "logout.php" not in r.text:
            banner("Échec d’authentification", "ERROR")
            return False

        banner("Authentification réussie", "OK")
        return _set_security("low")

    except requests.RequestException as e:
        banner(f"Erreur de connexion DVWA : {e}", "ERROR")
        return False

def _set_security(level: str = "low") -> bool:
    sec_url = f"http://{config.TARGET_IP}:{config.TARGET_PORT}/dvwa/security.php"
    try:
        r = session.get(sec_url, timeout=5)
        token = _extract_token(r.text)

        payload = {
            "security":       level,
            "seclev_submit":  "Submit",
            "user_token":     token
        }
        r = session.post(sec_url, data=payload, timeout=5)
        if f"Security level set to {level}" in r.text:
            banner(f"Niveau de sécurité DVWA ⇒ {level}", "OK")
            return True
        banner("Impossible de changer le niveau de sécurité", "WARN")
    except requests.RequestException as e:
        banner(f"Erreur réglage sécurité : {e}", "ERROR")
    return False
