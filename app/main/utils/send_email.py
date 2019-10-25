from flask import render_template
from flask_mail import Message
from .. import mail


def send_email(subject, recipients, data, sender, template_path):
    message = Message(
        subject=subject,
        recipients=recipients,
        html=render_template(template_path, data=data),
        sender=sender)
    return mail.send(message)
