"""Test simple de la connexion SQLAlchemy."""

import sys
sys.path.append('C:\\Users\\Admin\\Desktop\\YOK2\\BACKEND')

from sqlalchemy import text
from shared.db.conn import SessionLocale

def tester_connexion():
    """Teste la connexion à PostgreSQL avec SQLAlchemy."""
    print("🔄 Test de connexion SQLAlchemy...")
    
    try:
        # Créer une session
        session = SessionLocale()
        
        # Requête simple pour tester
        resultat = session.execute(text("SELECT version();"))
        version = resultat.fetchone()[0]
        
        print(f"✅ Connexion réussie!")
        print(f"📊 PostgreSQL version: {version}")
        
        session.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {type(e).__name__}")
        print(f"📝 Message: {e}")
        return False

if __name__ == "__main__":
    tester_connexion()
