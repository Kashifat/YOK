class Settings:
	"""Configuration du microservice catalogue."""

	app_name: str = "Service Catalogue"
	jwt_secret_key: str = "9f3d7c8a2e1b4f6d9c5e3a1b7f4d8c2e9a5b3f6e1d4c8a2f7b5e9c3a1d6f4"
	jwt_algorithm: str = "HS256"


settings = Settings()
