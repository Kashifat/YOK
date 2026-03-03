import os


class Settings:
	"""Configuration du microservice paiement."""

	app_name: str = "Service Paiement"
	jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "")
	jwt_algorithm: str = "HS256"

	cinetpay_api_key: str = os.getenv("CINETPAY_API_KEY", "")
	cinetpay_site_id: str = os.getenv("CINETPAY_SITE_ID", "")
	cinetpay_api_url: str = os.getenv("CINETPAY_API_URL", "https://api-checkout.cinetpay.com/v2/payment")
	cinetpay_check_url: str = os.getenv("CINETPAY_CHECK_URL", "https://api-checkout.cinetpay.com/v2/payment/check")
	cinetpay_notify_url: str = os.getenv("CINETPAY_NOTIFY_URL", "http://localhost:8006/paiements/webhooks/cinetpay")
	cinetpay_return_url: str = os.getenv("CINETPAY_RETURN_URL", "http://localhost:3000/paiement/retour")
	cinetpay_webhook_secret: str = os.getenv("CINETPAY_WEBHOOK_SECRET", "")


settings = Settings()
