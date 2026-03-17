import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
	"""Configuration du microservice paiement."""

	app_name: str = "Service Paiement Clients"
	jwt_secret_key: str = os.getenv(
		"AUTH_JWT_SECRET_KEY",
		os.getenv("JWT_SECRET_KEY", "9f3d7c8a2e1b4f6d9c5e3a1b7f4d8c2e9a5b3f6e1d4c8a2f7b5e9c3a1d6f4"),
	)
	jwt_algorithm: str = os.getenv("AUTH_JWT_ALGORITHM", os.getenv("JWT_ALGORITHM", "HS256"))

	cinetpay_api_key: str = os.getenv("CINETPAY_API_KEY", "")
	cinetpay_site_id: str = os.getenv("CINETPAY_SITE_ID", "")
	cinetpay_api_url: str = os.getenv("CINETPAY_API_URL", "https://api-checkout.cinetpay.com/v2/payment")
	cinetpay_check_url: str = os.getenv("CINETPAY_CHECK_URL", "https://api-checkout.cinetpay.com/v2/payment/check")
	cinetpay_notify_url: str = os.getenv("CINETPAY_NOTIFY_URL", "http://localhost:8006/paiements/webhooks/cinetpay")
	cinetpay_return_url: str = os.getenv("CINETPAY_RETURN_URL", "http://localhost:3000/paiement/retour")
	cinetpay_webhook_secret: str = os.getenv("CINETPAY_WEBHOOK_SECRET", "")


settings = Settings()
