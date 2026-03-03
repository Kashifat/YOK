from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session

from shared.db.conn import obtenir_session

from ..schemas.user import TokenPaire
from ..services.auth_service import AuthService
from ..services.oauth_service import OAuthService


router = APIRouter(tags=["OAuth"])

# Configuration du frontend
FRONTEND_URL = "http://localhost:3000"  # Changer selon votre config


# ========== GOOGLE ==========

@router.get("/oauth/google")
def google_login():
	"""Redirige vers Google pour l'authentification."""
	auth_url = OAuthService.get_google_auth_url()
	return RedirectResponse(auth_url)


@router.get("/oauth/google/callback")
async def google_callback(code: str, state: str = None, db: Session = Depends(obtenir_session)):
	"""Callback Google : échange le code contre un JWT et redirige vers le frontend."""
	try:
		# Récupérer les infos utilisateur depuis Google
		oauth_data = await OAuthService.exchange_google_code(code)
		
		# Connecter ou créer l'utilisateur
		service = AuthService(db)
		tokens = service.oauth_login_ou_inscription(oauth_data)
		
		# Rediriger vers le frontend avec les tokens
		return RedirectResponse(
			url=f"{FRONTEND_URL}?access_token={tokens.access_token}&refresh_token={tokens.refresh_token}",
			status_code=303
		)
	except HTTPException as e:
		# En cas d'erreur, afficher un message
		return HTMLResponse(
			f"""
			<html>
				<head>
					<title>Erreur OAuth</title>
					<style>
						body {{ font-family: Arial; text-align: center; padding: 50px; }}
						.error {{ background: #f8d7da; padding: 20px; border-radius: 5px; }}
					</style>
				</head>
				<body>
					<div class="error">
						<h2>❌ Erreur d'authentification</h2>
						<p>{e.detail}</p>
						<p><a href="{FRONTEND_URL}">Retourner au login</a></p>
					</div>
				</body>
			</html>
			"""
		)


# ========== FACEBOOK ==========

@router.get("/oauth/facebook")
def facebook_login():
	"""Redirige vers Facebook pour l'authentification."""
	auth_url = OAuthService.get_facebook_auth_url()
	return RedirectResponse(auth_url)


@router.get("/oauth/facebook/callback")
async def facebook_callback(code: str, state: str = None, db: Session = Depends(obtenir_session)):
	"""Callback Facebook : échange le code contre un JWT et redirige vers le frontend."""
	try:
		# Récupérer les infos utilisateur depuis Facebook
		oauth_data = await OAuthService.exchange_facebook_code(code)
		
		# Connecter ou créer l'utilisateur
		service = AuthService(db)
		tokens = service.oauth_login_ou_inscription(oauth_data)
		
		# Rediriger vers le frontend avec les tokens
		return RedirectResponse(
			url=f"{FRONTEND_URL}?access_token={tokens.access_token}&refresh_token={tokens.refresh_token}",
			status_code=303
		)
	except HTTPException as e:
		# En cas d'erreur, afficher un message
		return HTMLResponse(
			f"""
			<html>
				<head>
					<title>Erreur OAuth</title>
					<style>
						body {{ font-family: Arial; text-align: center; padding: 50px; }}
						.error {{ background: #f8d7da; padding: 20px; border-radius: 5px; }}
					</style>
				</head>
				<body>
					<div class="error">
						<h2>❌ Erreur d'authentification</h2>
						<p>{e.detail}</p>
						<p><a href="{FRONTEND_URL}">Retourner au login</a></p>
					</div>
				</body>
			</html>
			"""
		)
