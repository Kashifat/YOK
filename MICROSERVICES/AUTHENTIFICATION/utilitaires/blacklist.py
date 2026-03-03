# Blacklist simple en mémoire pour logout (à remplacer par Redis en prod)
blacklist_tokens: set[str] = set()


def ajouter_blacklist(token: str) -> None:
    """Ajoute un token à la blacklist (logout)."""
    blacklist_tokens.add(token)


def est_blacklist(token: str) -> bool:
    """Vérifie si un token est blacklisté."""
    return token in blacklist_tokens
