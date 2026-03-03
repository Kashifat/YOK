"""
Lanceur du service d'authentification
Utilise: python -m MICROSERVICES.AUTHENTIFICATION
"""

import sys
from pathlib import Path

# Ajouter le chemin parent pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from MICROSERVICES.AUTHENTIFICATION.main import creer_application
import uvicorn

if __name__ == "__main__":
    app = creer_application()
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001,
        reload=True
    )
