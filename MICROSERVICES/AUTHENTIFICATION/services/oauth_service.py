"""Service OAuth pour Google et Facebook."""

import httpx
from fastapi import HTTPException, status

from ..config import settings
from ..schemas.user import OAuthUserData


class OAuthService:
	"""Gère l'authentification OAuth avec Google et Facebook."""

	@staticmethod
	def get_google_auth_url() -> str:
		"""Génère l'URL de redirection Google OAuth."""
		base_url = "https://accounts.google.com/o/oauth2/v2/auth"
		params = {
			"client_id": settings.google_client_id,
			"redirect_uri": settings.google_redirect_uri,
			"response_type": "code",
			"scope": "openid email profile",
			"access_type": "offline",
			"prompt": "consent"
		}
		query = "&".join([f"{k}={v}" for k, v in params.items()])
		return f"{base_url}?{query}"

	@staticmethod
	def get_facebook_auth_url() -> str:
		"""Génère l'URL de redirection Facebook OAuth."""
		base_url = "https://www.facebook.com/v18.0/dialog/oauth"
		params = {
			"client_id": settings.facebook_client_id,
			"redirect_uri": settings.facebook_redirect_uri,
			"scope": "email,public_profile"
		}
		query = "&".join([f"{k}={v}" for k, v in params.items()])
		return f"{base_url}?{query}"

	@staticmethod
	async def exchange_google_code(code: str) -> OAuthUserData:
		"""Échange le code Google contre les infos utilisateur."""
		# Échanger le code contre un access token
		token_url = "https://oauth2.googleapis.com/token"
		token_data = {
			"code": code,
			"client_id": settings.google_client_id,
			"client_secret": settings.google_client_secret,
			"redirect_uri": settings.google_redirect_uri,
			"grant_type": "authorization_code"
		}

		async with httpx.AsyncClient() as client:
			token_response = await client.post(token_url, data=token_data)
			if token_response.status_code != 200:
				raise HTTPException(
					status_code=status.HTTP_400_BAD_REQUEST,
					detail="Erreur lors de l'authentification Google"
				)
			
			token_json = token_response.json()
			access_token = token_json.get("access_token")

			# Récupérer les infos utilisateur
			user_url = "https://www.googleapis.com/oauth2/v2/userinfo"
			headers = {"Authorization": f"Bearer {access_token}"}
			user_response = await client.get(user_url, headers=headers)
			
			if user_response.status_code != 200:
				raise HTTPException(
					status_code=status.HTTP_400_BAD_REQUEST,
					detail="Impossible de récupérer les informations utilisateur"
				)
			
			user_data = user_response.json()
			
			return OAuthUserData(
				email=user_data.get("email"),
				name=user_data.get("name"),
				picture=user_data.get("picture"),
				provider="google",
				provider_user_id=user_data.get("id")
			)

	@staticmethod
	async def exchange_facebook_code(code: str) -> OAuthUserData:
		"""Échange le code Facebook contre les infos utilisateur."""
		# Échanger le code contre un access token
		token_url = "https://graph.facebook.com/v18.0/oauth/access_token"
		token_params = {
			"client_id": settings.facebook_client_id,
			"client_secret": settings.facebook_client_secret,
			"redirect_uri": settings.facebook_redirect_uri,
			"code": code
		}

		async with httpx.AsyncClient() as client:
			token_response = await client.get(token_url, params=token_params)
			if token_response.status_code != 200:
				raise HTTPException(
					status_code=status.HTTP_400_BAD_REQUEST,
					detail="Erreur lors de l'authentification Facebook"
				)
			
			token_json = token_response.json()
			access_token = token_json.get("access_token")

			# Récupérer les infos utilisateur
			user_url = "https://graph.facebook.com/me"
			user_params = {
				"fields": "id,name,email,picture",
				"access_token": access_token
			}
			user_response = await client.get(user_url, params=user_params)
			
			if user_response.status_code != 200:
				raise HTTPException(
					status_code=status.HTTP_400_BAD_REQUEST,
					detail="Impossible de récupérer les informations utilisateur"
				)
			
			user_data = user_response.json()
			
			return OAuthUserData(
				email=user_data.get("email"),
				name=user_data.get("name"),
				picture=user_data.get("picture", {}).get("data", {}).get("url"),
				provider="facebook",
				provider_user_id=user_data.get("id")
			)
