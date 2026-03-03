from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .controllers.livraison import router as livraison_router


def creer_application() -> FastAPI:
	app = FastAPI(title=settings.app_name)

	app.add_middleware(
		CORSMiddleware,
		allow_origins=["*"],
		allow_credentials=True,
		allow_methods=["*"],
		allow_headers=["*"],
	)

	app.include_router(livraison_router, prefix="/livraisons", tags=["Livraisons"])

	@app.get("/health")
	def healthcheck():
		return {"status": "ok", "service": "livraison"}

	return app


app = creer_application()
