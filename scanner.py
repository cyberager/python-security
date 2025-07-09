import dvwa                 # <— NOUVEAU
from bs4 import BeautifulSoup
from utils import banner
import config

def check_http() -> bool:
    if not dvwa.login():     # <— connexion avant tout
        return False

    url = f"http://{config.TARGET_IP}:{config.TARGET_PORT}{config.VULN_PATH}"
    banner(f"Test d’accès à {url}")
    try:
        r = dvwa.session.get(url, timeout=5)          # <— on réutilise la session
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")
            title = soup.title.string if soup.title else "Sans titre"
            banner(f"Page accessible : « {title} »", "OK")
            return True
        banner(f"Code HTTP inattendu : {r.status_code}", "WARN")
    except requests.RequestException as e:
        banner(f"Erreur HTTP : {e}", "ERROR")
    return False
