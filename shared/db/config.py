"""Configuration de la base de données PostgreSQL."""

import os
from pathlib import Path
from urllib.parse import quote_plus


def _charger_env_backend() -> None:
    """Charge le fichier .env racine BACKEND dans os.environ (sans écraser l'existant)."""
    racine_backend = Path(__file__).resolve().parents[2]
    env_path = racine_backend / ".env"
    if not env_path.exists():
        return

    for ligne in env_path.read_text(encoding="utf-8").splitlines():
        ligne = ligne.strip()
        if not ligne or ligne.startswith("#") or "=" not in ligne:
            continue

        cle, valeur = ligne.split("=", 1)
        cle = cle.strip()
        valeur = valeur.strip().strip('"').strip("'")

        if cle and cle not in os.environ:
            os.environ[cle] = valeur


def _get_env(*cles: str, default: str = "") -> str:
    for cle in cles:
        valeur = os.getenv(cle)
        if valeur is not None and valeur != "":
            return valeur
    return default


_charger_env_backend()

class ConfigurationBD:
    """Paramètres de connexion PostgreSQL."""
    HOTE = _get_env("DB_HOST", "BD_HOTE", default="localhost")
    PORT = int(_get_env("DB_PORT", "BD_PORT", default="5432"))
    NOM = _get_env("DB_NAME", "BD_NOM", default="yok_bd")
    UTILISATEUR = _get_env("DB_USER", "BD_UTILISATEUR", default="postgres")
    MOT_DE_PASSE = _get_env("DB_PASSWORD", "BD_MOT_DE_PASSE", default="")

    @staticmethod
    def url_postgres(avec_mot_de_passe: bool = True) -> str:
        """Construit l'URL de connexion PostgreSQL."""
        if not avec_mot_de_passe or not ConfigurationBD.MOT_DE_PASSE:
            return (
                f"postgresql://{ConfigurationBD.UTILISATEUR}@"
                f"{ConfigurationBD.HOTE}:{ConfigurationBD.PORT}/"
                f"{ConfigurationBD.NOM}"
            )

        mot_de_passe_encode = quote_plus(ConfigurationBD.MOT_DE_PASSE)
        return (
            f"postgresql://{ConfigurationBD.UTILISATEUR}:"
            f"{mot_de_passe_encode}@"
            f"{ConfigurationBD.HOTE}:{ConfigurationBD.PORT}/"
            f"{ConfigurationBD.NOM}"
        )

    @staticmethod
    def urls_candidates() -> list[str]:
        """Retourne une liste d'URLs candidates (avec/sans mot de passe)."""
        urls: list[str] = []

        if ConfigurationBD.MOT_DE_PASSE:
            urls.append(ConfigurationBD.url_postgres(avec_mot_de_passe=True))

        url_sans_mdp = ConfigurationBD.url_postgres(avec_mot_de_passe=False)
        if url_sans_mdp not in urls:
            urls.append(url_sans_mdp)

        return urls
