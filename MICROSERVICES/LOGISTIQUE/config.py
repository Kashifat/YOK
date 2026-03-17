import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
	"""Configuration du microservice logistique."""

	app_name: str = "Service Logistique"
	jwt_secret_key: str = os.getenv(
		"AUTH_JWT_SECRET_KEY",
		os.getenv("JWT_SECRET_KEY", "9f3d7c8a2e1b4f6d9c5e3a1b7f4d8c2e9a5b3f6e1d4c8a2f7b5e9c3a1d6f4"),
	)
	jwt_algorithm: str = os.getenv("AUTH_JWT_ALGORITHM", os.getenv("JWT_ALGORITHM", "HS256"))


settings = Settings()
