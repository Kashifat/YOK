import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
	"""Configuration du microservice d'authentification."""

	app_name: str = "Service Authentification"
	jwt_secret_key: str = os.getenv(
		"AUTH_JWT_SECRET_KEY",
		os.getenv("JWT_SECRET_KEY", "9f3d7c8a2e1b4f6d9c5e3a1b7f4d8c2e9a5b3f6e1d4c8a2f7b5e9c3a1d6f4"),
	)
	jwt_algorithm: str = os.getenv("AUTH_JWT_ALGORITHM", os.getenv("JWT_ALGORITHM", "HS256"))
	access_token_expire_minutes: int = int(os.getenv("AUTH_ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
	refresh_token_expire_days: int = int(os.getenv("AUTH_REFRESH_TOKEN_EXPIRE_DAYS", "7"))
	rate_limit_login: int = 5
	
	# OAuth Google
	google_client_id: str = os.getenv("GOOGLE_CLIENT_ID", "VOTRE_GOOGLE_CLIENT_ID")
	google_client_secret: str = os.getenv("GOOGLE_CLIENT_SECRET", "VOTRE_GOOGLE_CLIENT_SECRET")
	google_redirect_uri: str = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8001/auth/oauth/google/callback")
	
	# OAuth Facebook
	facebook_client_id: str = os.getenv("FACEBOOK_CLIENT_ID", "VOTRE_FACEBOOK_CLIENT_ID")
	facebook_client_secret: str = os.getenv("FACEBOOK_CLIENT_SECRET", "VOTRE_FACEBOOK_CLIENT_SECRET")
	facebook_redirect_uri: str = os.getenv("FACEBOOK_REDIRECT_URI", "http://localhost:8001/auth/oauth/facebook/callback")


settings = Settings()
