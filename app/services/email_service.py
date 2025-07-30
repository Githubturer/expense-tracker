from email.message import EmailMessage
from aiosmtplib import SMTP, SMTPException
from app.core import settings
from app.core.security import create_token
from app.constants import TokenType
from app.models.user import User
from app.schemas.email import EmailVerification
import logging

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(
        self,
        smtp_host: str = settings.mail_server,
        smtp_port: int = settings.mail_port,
        smtp_username: str = settings.mail_username,
        smtp_password: str = settings.mail_password,
        from_email: str = settings.mail_from,
        use_tls: bool = settings.mail_use_tls,
        use_ssl: bool = settings.mail_use_ssl,
    ):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password
        self.from_email = from_email
        self.use_tls = use_tls
        self.use_ssl = use_ssl

    async def send_email(self, email: EmailVerification) -> None:
        message = EmailMessage()
        message["From"] = self.from_email
        message["To"] = ", ".join(email.to)  #više korisnika
        message["Subject"] = email.subject
        message.set_content(email.body)

        smtp = SMTP(
            hostname=self.smtp_host,
            port=self.smtp_port,
            use_tls=self.use_ssl,  
        )

        try:
            await smtp.connect()
            if self.use_tls and not self.use_ssl:
                await smtp.starttls()
            if self.smtp_username and self.smtp_password:
                await smtp.login(self.smtp_username, self.smtp_password)

            await smtp.send_message(message)
        except SMTPException as e:
            logger.warning(f"Failed to send email to {email.to}: {e}")
            raise e
        finally:
            await smtp.quit()

    async def send_verification_email(self, user: User) -> None:
        token = create_token(user, TokenType.VERIFICATION)
        verification_url = f"Use this verification token for the API endpoint: {token}"

        email_data = EmailVerification(
            subject="Email Verification Token",
            body=verification_url,
            to=[user.email],
        )
        await self.send_email(email_data)

    async def send_password_reset_email(self, user: User | None) -> None:
        #ako user ne postoji, nece se poslati email ali ni nece se baciti error. Vracamo 204 uvijek.
        if not user:
            return None
        token = create_token(user, TokenType.PASSWORD_RESET)
        password_reset_url = f"Use this password reset token for the API endpoint: {token}"

        email_data = EmailVerification(
            subject="Password Reset Token",
            body=password_reset_url,
            to=[user.email],
        )
        await self.send_email(email_data)

mail_service = EmailService()
