from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .controllers.client import router as client_router


def creer_application() -> FastAPI:
    app = FastAPI(title=settings.app_name)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(client_router, prefix="/favoris", tags=["Favoris"])

    @app.get("/health")
    def healthcheck():
        return {"status": "ok", "service": "favoris"}

    return app


app = creer_application()
