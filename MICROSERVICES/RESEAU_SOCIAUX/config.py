import os


class Settings:
	"""Configuration du microservice réseau sociaux."""

	app_name: str = "Service Reseau Sociaux"
	jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "")
	jwt_algorithm: str = "HS256"


settings = Settings()
