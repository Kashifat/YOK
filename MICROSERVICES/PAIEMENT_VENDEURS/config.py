import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
	"""Configuration du microservice paiement vendeurs."""

	app_name: str = "Service Paiement Vendeurs"
	jwt_secret_key: str = os.getenv(
		"AUTH_JWT_SECRET_KEY",
		os.getenv("JWT_SECRET_KEY", "9f3d7c8a2e1b4f6d9c5e3a1b7f4d8c2e9a5b3f6e1d4c8a2f7b5e9c3a1d6f4"),
	)
	jwt_algorithm: str = os.getenv("AUTH_JWT_ALGORITHM", os.getenv("JWT_ALGORITHM", "HS256"))

	commission_percent: float = float(os.getenv("WALLET_COMMISSION_PERCENT", "0.10"))
	# Modèle partiel : avance à l'expédition vendeur (20%), solde à la vérification agent (80%)
	avance_percent_expedition_vendeur: float = float(os.getenv("WALLET_AVANCE_PERCENT_EXPEDITION", "0.20"))
	solde_percent_verification_agent: float = float(os.getenv("WALLET_SOLDE_PERCENT_VERIFICATION", "0.80"))
	# Legacy (backward compat, non utilisé en V2)
	avance_percent_expediee: float = float(os.getenv("WALLET_AVANCE_PERCENT_EXPEDIEE", "0.60"))


settings = Settings()
