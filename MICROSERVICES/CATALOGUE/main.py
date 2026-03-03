from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .controllers.public import router as public_router
from .controllers.vendeur import router as vendeur_router
from .controllers.admin import router as admin_router


def creer_application() -> FastAPI:
	app = FastAPI(title=settings.app_name)

	app.add_middleware(
		CORSMiddleware,
		allow_origins=["*"],
		allow_credentials=True,
		allow_methods=["*"],
		allow_headers=["*"],
	)

	app.include_router(public_router, prefix="/catalogue/public", tags=["Catalogue Public"])
	app.include_router(vendeur_router, prefix="/catalogue/vendeur", tags=["Catalogue Vendeur"])
	app.include_router(admin_router, prefix="/catalogue/admin", tags=["Catalogue Admin"])

	@app.get("/health")
	def healthcheck():
		return {"status": "ok"}

	return app


app = creer_application()
