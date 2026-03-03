from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .controllers.wallet import router as wallet_router


def creer_application() -> FastAPI:
	app = FastAPI(title=settings.app_name)

	app.add_middleware(
		CORSMiddleware,
		allow_origins=["*"],
		allow_credentials=True,
		allow_methods=["*"],
		allow_headers=["*"],
	)

	app.include_router(wallet_router, prefix="/wallet-vendeurs", tags=["Wallet Vendeurs"])

	@app.get("/health")
	def healthcheck():
		return {"status": "ok", "service": "paiement_vendeurs"}

	return app


app = creer_application()
