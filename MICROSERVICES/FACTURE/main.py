from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .controllers.facture import router as facture_router


def creer_application() -> FastAPI:
	app = FastAPI(title=settings.app_name)

	app.add_middleware(
		CORSMiddleware,
		allow_origins=["*"],
		allow_credentials=True,
		allow_methods=["*"],
		allow_headers=["*"],
	)

	app.include_router(facture_router, prefix="/factures", tags=["Factures"])

	@app.get("/health")
	def healthcheck():
		return {"status": "ok", "service": "facture"}

	return app


app = creer_application()
