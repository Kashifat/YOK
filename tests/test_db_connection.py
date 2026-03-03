#!/usr/bin/env python3
"""Test insertion utilisateur avec SQLAlchemy."""

import sys
sys.path.insert(0, 'C:\\Users\\Admin\\Desktop\\YOK2\\BACKEND')

from sqlalchemy import text
from shared.db.conn import SessionLocale
from shared.security.password import hash_password
import uuid

def test_insertion_utilisateur():
    """Test insertion d'un utilisateur."""
    print("=" * 60)
    print("TEST INSERTION UTILISATEUR")
    print("=" * 60)
    
    try:
        session = SessionLocale()
		
        # Supprimer si existe
        session.execute(text("DELETE FROM utilisateurs WHERE courriel = :courriel"), {"courriel": "test@example.com"})
		
        # Insérer nouvel utilisateur
        session.execute(text("""
            INSERT INTO utilisateurs 
            (identifiant, nom_complet, courriel, mot_de_passe_hash, telephone, role, est_actif)
            VALUES (:identifiant, :nom_complet, :courriel, :mot_de_passe_hash, :telephone, :role, :est_actif)
        """), {
            "identifiant": str(uuid.uuid4()),
            "nom_complet": "Test User",
            "courriel": "test@example.com",
            "mot_de_passe_hash": hash_password("TestPassword123"),
            "telephone": "0612345678",
            "role": "CLIENT",
            "est_actif": True
        })
        session.commit()
		
        print("✅ Insertion réussie!")
		
        # Vérifier
        result = session.execute(text("SELECT nom_complet, courriel, role FROM utilisateurs WHERE courriel = :courriel"), {"courriel": "test@example.com"})
        user = result.fetchone()
        print("✅ Utilisateur créé:")
        print(f"   Nom: {user[0]}")
        print(f"   Email: {user[1]}")
        print(f"   Rôle: {user[2]}")
		
        session.close()
        return True
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("\n🔍 TEST INSERTION UTILISATEUR\n")
    test_insertion_utilisateur()
    print("\n" + "=" * 60)

