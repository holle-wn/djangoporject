import os
import django
import smtplib
from helloword import settings

from email.mime.text import MIMEText

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'helloword.settings')
django.setup()


def send_mail():
    msg = MIMEText("邮件通道测试", "plain", "utf-8")
    msg['FROM'] = "Mail Test"
    msg['Subject'] = "【Mail Test】"
    receivers = ['发给谁']
    server = smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT)
    server.set_debuglevel(1)
    server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    server.sendmail(settings.EMAIL_FROM, receivers, msg.as_string())
    server.close()
    pass


if __name__ == '__main__':
    send_mail()
