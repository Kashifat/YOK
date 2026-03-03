import os


class Settings:
	"""Configuration du microservice paiement vendeurs."""

	app_name: str = "Service Paiement Vendeurs"
	jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "")
	jwt_algorithm: str = "HS256"

	commission_percent: float = float(os.getenv("WALLET_COMMISSION_PERCENT", "0.10"))
	avance_percent_expediee: float = float(os.getenv("WALLET_AVANCE_PERCENT_EXPEDIEE", "0.60"))


settings = Settings()
