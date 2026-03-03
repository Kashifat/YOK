"""
Application FastAPI pour le service NOTIFICATION
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from .config import SERVICE_NAME, SERVICE_PORT, LOG_LEVEL
from .controllers.commande import router as notification_router

# Configuration du logging
logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)

def creer_application() -> FastAPI:
    """Créer et configurer l'application FastAPI"""
    
    app = FastAPI(
        title=SERVICE_NAME,
        description="Service de notifications par email pour les commandes YOK",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # ==================== MIDDLEWARE ====================
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # ==================== ROUTERS ====================
    app.include_router(notification_router)
    
    # ==================== HEALTH CHECK ====================
    @app.get("/health", tags=["Health"])
    def health_check():
        """Vérifier la santé du service"""
        return {
            "status": "ok",
            "service": SERVICE_NAME,
            "port": SERVICE_PORT
        }
    
    @app.get("/", tags=["Root"])
    def root():
        """Endpoint racine"""
        return {
            "message": f"Service {SERVICE_NAME} actif",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    
    logger.info(f"Service {SERVICE_NAME} initialisé sur le port {SERVICE_PORT}")
    
    return app

# Créer l'application
app = creer_application()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8004,
        reload=True
    )
