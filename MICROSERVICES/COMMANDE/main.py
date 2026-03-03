from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .controllers.panier import router as panier_router
from .controllers.commande_client import router as commande_client_router
from .controllers.commande_vendeur import router as commande_vendeur_router
from .controllers.commande_admin import router as commande_admin_router


def creer_application() -> FastAPI:
	app = FastAPI(title=settings.app_name)

	app.add_middleware(
		CORSMiddleware,
		allow_origins=["*"],
		allow_credentials=True,
		allow_methods=["*"],
		allow_headers=["*"],
	)

	app.include_router(panier_router, prefix="/panier", tags=["Panier"])
	app.include_router(commande_client_router, prefix="/commandes/client", tags=["Commandes Client"])
	app.include_router(commande_vendeur_router, prefix="/commandes/vendeur", tags=["Commandes Vendeur"])
	app.include_router(commande_admin_router, prefix="/commandes/admin", tags=["Commandes Admin"])

	@app.get("/health")
	def healthcheck():
		return {"status": "ok"}

	return app


app = creer_application()
