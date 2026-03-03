"""Gestion des connexions PostgreSQL avec SQLAlchemy + psycopg3."""

import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session

from .config import ConfigurationBD

# FIX: Nettoyer les variables d'environnement problématiques
for var in ['LANG', 'LC_ALL', 'LC_CTYPE']:
    if var in os.environ:
        del os.environ[var]

def _masquer_url(url: str) -> str:
    if "@" not in url or ":" not in url.split("@", 1)[0]:
        return url
    prefixe, suffixe = url.split("@", 1)
    user = prefixe.split("//", 1)[-1].split(":", 1)[0]
    proto = prefixe.split("//", 1)[0] + "//"
    return f"{proto}{user}:***@{suffixe}"


def _creer_moteur_avec_fallback():
    erreurs: list[str] = []

    for url in ConfigurationBD.urls_candidates():
        url_psycopg3 = url.replace("postgresql://", "postgresql+psycopg://")
        try:
            engine = create_engine(url_psycopg3, pool_pre_ping=True, echo=False)
            with engine.connect() as connexion:
                connexion.execute(text("SELECT 1"))
            print(f"[DB] Connexion OK via {_masquer_url(url_psycopg3)}")
            return engine
        except Exception as exc:
            erreurs.append(f"- {_masquer_url(url_psycopg3)} -> {exc}")

    detail = "\n".join(erreurs)
    raise RuntimeError(
        "Impossible d'établir une connexion PostgreSQL avec les paramètres actuels.\n"
        f"Essais effectués:\n{detail}"
    )


# Moteur SQLAlchemy global avec psycopg3
moteur = _creer_moteur_avec_fallback()

# Fabrique de sessions
SessionLocale = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=moteur
)

def obtenir_session():
    """Dependency pour FastAPI - fournit une session SQLAlchemy."""
    session = SessionLocale()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


