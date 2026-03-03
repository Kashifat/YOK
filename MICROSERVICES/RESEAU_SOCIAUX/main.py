from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .controllers.social import router as social_router


def creer_application() -> FastAPI:
	app = FastAPI(title=settings.app_name)

	app.add_middleware(
		CORSMiddleware,
		allow_origins=["*"],
		allow_credentials=True,
		allow_methods=["*"],
		allow_headers=["*"],
	)

	app.include_router(social_router, prefix="/reseau", tags=["Réseau social"])

	@app.get("/health")
	def healthcheck():
		return {"status": "ok", "service": "reseau_sociaux"}

	return app


app = creer_application()
