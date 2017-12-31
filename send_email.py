from email.mime.text import MIMEText
import logging
from os import environ
import smtplib

logger = logging.getLogger()

recipient_email = environ['RECIPIENT_EMAIL']
smtp_server = environ['SMTP_SERVER']
smtp_username = environ['SMTP_USER']
smtp_password = environ['SMTP_PASSWORD']


def send_email(name=None, email=None, phone=None,
               company=None, message=None):
    message = 'New email from {}\n' \
              '------------------------------\n' \
              'Email:   {}\n' \
              'Phone:   {}\n' \
              'Company: {}\n' \
              'Message:\n' \
              '-----------\n' \
              '{}'.format(name, email, phone, company, message)
    msg = MIMEText(message)
    msg['Subject'] = 'Website Contact Form Submission - {}'.format(name)
    msg['From'] = smtp_username
    msg['To'] = recipient_email
    try:
        s = smtplib.SMTP(smtp_server, 587)
        s.ehlo()
        s.starttls()
        s.login(smtp_username, smtp_password)
        s.sendmail(recipient_email, recipient_email, msg.as_string())
        s.close()
        status = True
    except Exception as s_error:
        logger.error("SMTP ERROR: {}".format(s_error))
        status = False
    return status
