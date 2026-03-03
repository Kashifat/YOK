import os


class Settings:
	"""Configuration du microservice facture."""

	app_name: str = "Service Facture"
	jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "")
	jwt_algorithm: str = "HS256"


settings = Settings()
