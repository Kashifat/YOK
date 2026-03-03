from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from .config import settings
from .controllers.auth import router as auth_router
from .controllers.oauth import router as oauth_router


def creer_application() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version="1.0.0"
    )

    # CORS - Autoriser les requêtes depuis le navigateur
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(
        auth_router,
        prefix="/auth",
        tags=["Authentification"]
    )
    
    app.include_router(
        oauth_router,
        prefix="/auth",
        tags=["OAuth"]
    )

    @app.get("/health", tags=["Health"])
    def healthcheck():
        return {"status": "ok"}

    return app


app = creer_application()


if __name__ == "__main__":
    uvicorn.run(
        "MICROSERVICES.AUTHENTIFICATION.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
