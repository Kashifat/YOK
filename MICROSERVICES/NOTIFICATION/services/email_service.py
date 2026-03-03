"""
Service d'envoi d'emails avec Gmail SMTP
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class EmailService:
    """Service d'envoi d'emails via Gmail SMTP"""
    
    def __init__(self, gmail_user: str, gmail_app_password: str, email_from_name: str = "YOK"):
        """
        Initialiser le service email Gmail
        
        Args:
            gmail_user: Adresse Gmail (toncompte@gmail.com)
            gmail_app_password: Mot de passe d'application Gmail (16 caractères)
            email_from_name: Nom d'affichage de l'expéditeur
        """
        self.gmail_user = gmail_user
        self.gmail_app_password = gmail_app_password.replace(" ", "")  # Supprimer les espaces
        self.email_from_name = email_from_name
        self.email_from = f"{email_from_name} <{gmail_user}>"
        self.smtp_host = "smtp.gmail.com"
        self.smtp_port = 587
    
    async def envoyer_email(
        self,
        email_destinataire: str,
        sujet: str,
        contenu_html: str,
        contenu_texte: Optional[str] = None
    ) -> tuple[bool, Optional[str]]:
        """
        Envoyer un email via Gmail
        
        Args:
            email_destinataire: Email du destinataire
            sujet: Sujet de l'email
            contenu_html: Contenu HTML
            contenu_texte: Contenu en texte simple (optionnel)
        
        Returns:
            (succès, message_erreur)
        """
        try:
            # Créer le message
            message = MIMEMultipart("alternative")
            message["Subject"] = sujet
            message["From"] = self.email_from
            message["To"] = email_destinataire
            
            # Ajouter la version texte
            if contenu_texte:
                message.attach(MIMEText(contenu_texte, "plain", "utf-8"))
            else:
                # Fallback texte basique
                message.attach(MIMEText(sujet, "plain", "utf-8"))
            
            # Ajouter la version HTML
            message.attach(MIMEText(contenu_html, "html", "utf-8"))
            
            # Envoyer l'email via Gmail
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.gmail_user, self.gmail_app_password)
                server.sendmail(self.gmail_user, email_destinataire, message.as_string())
            
            logger.info(f"Email envoyé à {email_destinataire}")
            return True, None
            
        except smtplib.SMTPAuthenticationError as e:
            msg = f"Erreur d'authentification Gmail: {str(e)}. Vérifiez votre mot de passe d'application."
            logger.error(msg)
            return False, msg
        except smtplib.SMTPException as e:
            msg = f"Erreur SMTP Gmail: {str(e)}"
            logger.error(msg)
            return False, msg
        except Exception as e:
            msg = f"Erreur lors de l'envoi d'email: {str(e)}"
            logger.error(msg)
            return False, msg

class TemplateEmail:
    """Générateur de templates HTML pour les notifications"""
    
    @staticmethod
    def template_commande_confirmee(
        nom_client: str,
        numero_commande: str,
        montant_total: float,
        adresse_livraison: str
    ) -> str:
        """Template pour confirmation de commande"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #007bff; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background-color: #f9f9f9; }}
                .footer {{ text-align: center; padding: 10px; font-size: 12px; color: #666; }}
                .success {{ color: #28a745; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>✅ Commande Confirmée</h1>
                </div>
                <div class="content">
                    <p>Bonjour {nom_client},</p>
                    <p class="success">Votre commande a été confirmée avec succès!</p>
                    <p><strong>Numéro de commande:</strong> {numero_commande}</p>
                    <p><strong>Montant total:</strong> {montant_total:,.0f} FCFA</p>
                    <p><strong>Adresse de livraison:</strong> {adresse_livraison}</p>
                    <p>Vous recevrez prochainement une notification dès que votre commande sera préparée.</p>
                    <p>Merci d'avoir choisi YOK! 🙏</p>
                </div>
                <div class="footer">
                    <p>YOK - Marketplace Sénégalaise</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    @staticmethod
    def template_preparation_commencee(
        nom_client: str,
        numero_commande: str
    ) -> str:
        """Template pour début de préparation"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #ffc107; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background-color: #f9f9f9; }}
                .footer {{ text-align: center; padding: 10px; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📦 Préparation en cours</h1>
                </div>
                <div class="content">
                    <p>Bonjour {nom_client},</p>
                    <p>Votre commande <strong>#{numero_commande}</strong> est maintenant en cours de préparation.</p>
                    <p>Elle sera expédiée très bientôt et vous recevrez un avis de livraison.</p>
                    <p>Merci de votre patience! 🙂</p>
                </div>
                <div class="footer">
                    <p>YOK - Marketplace Sénégalaise</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    @staticmethod
    def template_en_livraison(
        nom_client: str,
        numero_commande: str,
        date_livraison_estimee: str
    ) -> str:
        """Template pour expédition"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #17a2b8; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background-color: #f9f9f9; }}
                .footer {{ text-align: center; padding: 10px; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🚚 En route vers vous!</h1>
                </div>
                <div class="content">
                    <p>Bonjour {nom_client},</p>
                    <p>Bonne nouvelle! Votre commande <strong>#{numero_commande}</strong> est en livraison.</p>
                    <p><strong>Date de livraison estimée:</strong> {date_livraison_estimee}</p>
                    <p>Préparez-vous à la réception! 📬</p>
                </div>
                <div class="footer">
                    <p>YOK - Marketplace Sénégalaise</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    @staticmethod
    def template_livree(
        nom_client: str,
        numero_commande: str
    ) -> str:
        """Template pour livraison complète"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #28a745; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background-color: #f9f9f9; }}
                .footer {{ text-align: center; padding: 10px; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>✅ Commande Livrée</h1>
                </div>
                <div class="content">
                    <p>Bonjour {nom_client},</p>
                    <p>Votre commande <strong>#{numero_commande}</strong> a été livrée avec succès! 🎉</p>
                    <p>Nous espérons que vous êtes satisfait. N'hésitez pas à nous donner votre avis!</p>
                    <p>À bientôt sur YOK! 😊</p>
                </div>
                <div class="footer">
                    <p>YOK - Marketplace Sénégalaise</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    @staticmethod
    def template_annulee(
        nom_client: str,
        numero_commande: str,
        raison: str
    ) -> str:
        """Template pour annulation"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #dc3545; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background-color: #f9f9f9; }}
                .footer {{ text-align: center; padding: 10px; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>❌ Commande Annulée</h1>
                </div>
                <div class="content">
                    <p>Bonjour {nom_client},</p>
                    <p>Votre commande <strong>#{numero_commande}</strong> a été annulée.</p>
                    <p><strong>Raison:</strong> {raison}</p>
                    <p>Si vous avez des questions, n'hésitez pas à nous contacter.</p>
                    <p>Cordialement,<br>L'équipe YOK</p>
                </div>
                <div class="footer">
                    <p>YOK - Marketplace Sénégalaise</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    @staticmethod
    def template_probleme(
        nom_client: str,
        numero_commande: str,
        message: str
    ) -> str:
        """Template pour problème/alerte"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #ff9800; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background-color: #f9f9f9; }}
                .footer {{ text-align: center; padding: 10px; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>⚠️ Alerte sur votre commande</h1>
                </div>
                <div class="content">
                    <p>Bonjour {nom_client},</p>
                    <p>Un problème a été rencontré avec votre commande <strong>#{numero_commande}</strong>.</p>
                    <p><strong>Détails:</strong> {message}</p>
                    <p>Notre équipe a été notifiée et s'efforcera de résoudre ce problème rapidement.</p>
                    <p>Nous vous contacterons très bientôt.</p>
                </div>
                <div class="footer">
                    <p>YOK - Marketplace Sénégalaise</p>
                </div>
            </div>
        </body>
        </html>
        """
