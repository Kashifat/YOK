from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .controllers.logistique import router as logistique_router


def creer_application() -> FastAPI:
	app = FastAPI(title=settings.app_name)

	app.add_middleware(
		CORSMiddleware,
		allow_origins=["*"],
		allow_credentials=True,
		allow_methods=["*"],
		allow_headers=["*"],
	)

	app.include_router(logistique_router, prefix="/logistique", tags=["Logistique"])

	@app.get("/health")
	def healthcheck():
		return {"status": "ok", "service": "logistique"}

	return app


app = creer_application()
