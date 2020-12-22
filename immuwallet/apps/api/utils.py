from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def mandar_email(assunto, conteudo, remetente):
    message = Mail(
        from_email=settings.EMAIL_FROM,
        to_emails=remetente,
        subject=assunto,
        html_content=conteudo)

    try:
        sg = SendGridAPIClient(settings.EMAIL_SENDGRID_KEY)
        response = sg.send(message)
    except Exception as e:
        print('erro ao mandar email: ', e)
