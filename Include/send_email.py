import smtplib
from email.message import EmailMessage
from string import Template
from pathlib import Path


def send_email(email, middle_height, count):
    html = Template(Path('./Include/email.html').read_text())

    email_msg = EmailMessage()
    email_msg['from'] = 'Data collector app'
    email_msg['to'] = email
    email_msg['subject'] = 'Height data'

    email_msg.set_content(html.substitute(av_hieght=middle_height, count=count), 'html')

    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login('<email_login>', '<email_password>')
        smtp.send_message(email_msg)
