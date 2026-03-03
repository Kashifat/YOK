#!/usr/bin/env python3
"""Test simple de connexion PostgreSQL avec SQLAlchemy."""

import sys
sys.path.insert(0, 'C:\\Users\\Admin\\Desktop\\YOK2\\BACKEND')

from sqlalchemy import text
from shared.db.conn import SessionLocale

def test_connexion_simple():
    """Test la connexion basique via SQLAlchemy."""
    print("=" * 60)
    print("TEST CONNEXION SQLALCHEMY SIMPLE")
    print("=" * 60)
    
    try:
        session = SessionLocale()
        print("✅ Connexion réussie!")
		
        # Test simple
        result = session.execute(text("SELECT 1 as test"))
        print(f"✅ Requête réussie: {result.fetchone()}")
		
        # Test tables
        result = session.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """))
        tables = result.fetchall()
        print(f"✅ Tables existantes ({len(tables)}):")
        for table in tables:
            print(f"   - {table[0]}")
		
        session.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("\n🔍 TEST CONNEXION POSTGRESQL\n")
    if test_connexion_simple():
        print("\n✅ Connexion fonctionne parfaitement!")
    else:
        print("\n❌ Problème de connexion")
