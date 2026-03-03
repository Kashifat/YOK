"""
Test de vérification du flux OAuth - Google & Facebook
"""

import sys
from pathlib import Path

# Setup path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Vérifie que tous les imports fonctionnent."""
    print("🔍 Test 1: Vérification des imports...")
    try:
        from MICROSERVICES.AUTHENTIFICATION.services.oauth_service import OAuthService
        from MICROSERVICES.AUTHENTIFICATION.controllers.oauth import router
        from MICROSERVICES.AUTHENTIFICATION.services.auth_service import AuthService
        from MICROSERVICES.AUTHENTIFICATION.schemas.user import OAuthUserData, TokenPaire
        from MICROSERVICES.AUTHENTIFICATION.models.user import Utilisateur, RoleUtilisateur
        print("   ✅ Tous les imports OK\n")
        return True
    except Exception as e:
        print(f"   ❌ Erreur d'import: {e}\n")
        return False


def test_oauth_service():
    """Vérifie que le service OAuth est configuré."""
    print("🔍 Test 2: Configuration OAuth Service...")
    try:
        from MICROSERVICES.AUTHENTIFICATION.config import settings
        
        # Vérifier Google
        assert settings.google_client_id != "VOTRE_GOOGLE_CLIENT_ID", "❌ Google Client ID pas configuré"
        assert settings.google_client_secret, "❌ Google Client Secret vide"
        assert settings.google_redirect_uri, "❌ Google Redirect URI vide"
        print(f"   ✅ Google: Client ID = {settings.google_client_id[:20]}...")
        print(f"   ✅ Google: Redirect URI = {settings.google_redirect_uri}")
        
        # Vérifier Facebook (optionnel)
        if settings.facebook_client_id == "VOTRE_FACEBOOK_CLIENT_ID":
            print(f"   ⚠️  Facebook: Pas encore configuré\n")
        else:
            print(f"   ✅ Facebook: OK\n")
        return True
    except Exception as e:
        print(f"   ❌ Erreur: {e}\n")
        return False


def test_oauth_urls():
    """Vérifie la génération des URLs OAuth."""
    print("🔍 Test 3: Génération des URLs OAuth...")
    try:
        from MICROSERVICES.AUTHENTIFICATION.services.oauth_service import OAuthService
        
        google_url = OAuthService.get_google_auth_url()
        assert "accounts.google.com" in google_url, "❌ URL Google invalide"
        assert "client_id=" in google_url, "❌ Client ID manquant dans URL"
        print(f"   ✅ Google URL générée: {google_url[:60]}...")
        
        facebook_url = OAuthService.get_facebook_auth_url()
        assert "facebook.com" in facebook_url, "❌ URL Facebook invalide"
        print(f"   ✅ Facebook URL générée: {facebook_url[:60]}...")
        print()
        return True
    except Exception as e:
        print(f"   ❌ Erreur: {e}\n")
        return False


def test_oauth_schema():
    """Vérifie les schémas OAuth."""
    print("🔍 Test 4: Validation des schémas OAuth...")
    try:
        from MICROSERVICES.AUTHENTIFICATION.schemas.user import OAuthUserData, OAuthCallback
        
        # Créer un objet OAuthUserData
        oauth_user = OAuthUserData(
            email="test@example.com",
            name="Test User",
            picture="https://example.com/photo.jpg",
            provider="google",
            provider_user_id="123456789"
        )
        assert oauth_user.email == "test@example.com"
        assert oauth_user.provider == "google"
        print(f"   ✅ OAuthUserData valide")
        
        # Créer un objet OAuthCallback
        callback = OAuthCallback(code="abc123def456", state="xyz")
        assert callback.code == "abc123def456"
        print(f"   ✅ OAuthCallback valide")
        print()
        return True
    except Exception as e:
        print(f"   ❌ Erreur: {e}\n")
        return False


def test_routes():
    """Vérifie que les routes OAuth sont définies."""
    print("🔍 Test 5: Routes OAuth définies...")
    try:
        from MICROSERVICES.AUTHENTIFICATION.controllers.oauth import router
        
        # Vérifier que le router a des routes
        assert len(router.routes) > 0, "❌ Aucune route dans le router"
        
        routes = [r.path for r in router.routes]
        assert any("/oauth/google" in r for r in routes), "❌ Route /oauth/google manquante"
        assert any("/oauth/facebook" in r for r in routes), "❌ Route /oauth/facebook manquante"
        
        print(f"   ✅ Routes OAuth définies:")
        for route in router.routes:
            print(f"      - {route.methods} {route.path}")
        print()
        return True
    except Exception as e:
        print(f"   ❌ Erreur: {e}\n")
        return False


def main():
    print("\n" + "="*60)
    print("🧪 VÉRIFICATION COMPLÈTE OAUTH - GOOGLE & FACEBOOK")
    print("="*60 + "\n")
    
    results = []
    results.append(("Imports", test_imports()))
    results.append(("Configuration", test_oauth_service()))
    results.append(("URLs OAuth", test_oauth_urls()))
    results.append(("Schémas", test_oauth_schema()))
    results.append(("Routes", test_routes()))
    
    # Résumé
    print("="*60)
    print("📊 RÉSUMÉ")
    print("="*60)
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status:8} - {name}")
    
    all_passed = all(result for _, result in results)
    print("\n" + ("="*60))
    if all_passed:
        print("🎉 TOUS LES TESTS PASSENT - OAUTH PRÊT!")
    else:
        print("⚠️  CERTAINS TESTS ONT ÉCHOUÉ")
    print("="*60 + "\n")
    
    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
