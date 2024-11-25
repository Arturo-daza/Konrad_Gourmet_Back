import smtplib
from email.mime.text import MIMEText
from ssl import create_default_context

class ExternalService:
    """Interfaz base para adaptadores externos."""
    def enviar_correo(self, destinatario: str, asunto: str, mensaje: str):
        raise NotImplementedError("Este método debe ser implementado por subclases")

class EmailAdapter(ExternalService):
    """
    Adaptador para enviar correos electrónicos utilizando SMTP.
    """
    def __init__(self, sender_email: str, password: str):
        self.sender_email = sender_email
        self.password = password

    def enviar_correo(self, destinatario: str, asunto: str, mensaje: str):
        try:
            # Configuración del mensaje
            msg = MIMEText(mensaje)
            msg["Subject"] = asunto
            msg["From"] = self.sender_email
            msg["To"] = destinatario

            # Contexto SSL para la conexión segura
            context = create_default_context()

            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(self.sender_email, self.password)
                server.sendmail(self.sender_email, destinatario, msg.as_string())
                print(f"Correo enviado a {destinatario}")
        except Exception as e:
            print(f"Error al enviar correo: {str(e)}")
