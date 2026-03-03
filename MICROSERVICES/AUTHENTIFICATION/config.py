import os


class Settings:
	"""Configuration du microservice d'authentification."""

	app_name: str = "Service Authentification"
	jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "change_me_in_env")
	jwt_algorithm: str = "HS256"
	access_token_expire_minutes: int = 15
	refresh_token_expire_days: int = 7
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
