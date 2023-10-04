from django.conf import settings
from core.cadastros.models import Aluno
from core.loggingMe import logger
from celery import shared_task
import smtplib
from email.mime.text import MIMEText
from time import sleep


@shared_task()
def send_email(email_address):
    print('send_email chamado')
    sleep(5)  # Simular operação(ões) cara(s) que congela(m) o Django
    print(f'Envio de correio eletrónico para: {email_address}')
    me = settings.EMAIL_USERNAME
    password = settings.EMAIL_PASSWORD
    you = email_address

    email_body = """
    <html><body><p>Bem Vindo</p>
    </body></html>
    """

    message = MIMEText(email_body, 'html')

    message['Subject'] = f'New mail!'
    message['From'] = me
    message['To'] = you
    try:
        print('Trying to send an email')
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(me, password)
        server.sendmail(me, you, message.as_string())
        server.quit()
        print(f'Email sent: {email_body}')
    except Exception as e:
        print(f'Error in sending email: {e}')