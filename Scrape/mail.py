import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_log(from_mail, password, to_mail, subject, body):
    msg = MIMEMultipart()
    msg['From'] = from_mail
    msg['To'] = to_mail
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(from_mail, password)
    text = msg.as_string()
    server.sendmail(from_mail, to_mail, text)
    server.quit()
