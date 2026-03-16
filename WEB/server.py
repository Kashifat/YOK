"""
Serveur de développement pour le frontend test d'authentification
Sert les fichiers HTML/CSS/JS depuis le dossier WEB
"""

import http.server
import socketserver
import os
from pathlib import Path

PORT = 3000
WEB_DIR = Path(__file__).parent

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEB_DIR), **kwargs)
    
    def end_headers(self):
        # Ajouter headers CORS
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()


if __name__ == '__main__':
    os.chdir(WEB_DIR)
    
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"🚀 Serveur frontend démarré sur http://localhost:{PORT}")
        print(f"📁 Servant les fichiers depuis: {WEB_DIR}")
        print(f"\n💡 Ouvre http://localhost:{PORT} dans ton navigateur")
        print(f"\n📝 Teste:")
        print(f"   - Inscription classique (CLIENT, VENDEUR, ADMIN)")
        print(f"   - Connexion classique")
        print(f"   - OAuth Google")
        print(f"   - OAuth Facebook")
        print(f"\nAppuie sur Ctrl+C pour arrêter le serveur")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n❌ Serveur arrêté")
