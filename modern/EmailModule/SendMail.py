import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup as bs

#def sendMail(email, password, TO, subject):
def sendMail(email, password, TO, subject, html):
    # email = "dpeastudent7266@gmail.com"
    # password = "dpea7266!"

    FROM = email

    # TO = "2nikhilg@gmail.com"

    # subject = "hello"

    msg = MIMEMultipart("alternative")

    msg["From"] = FROM

    msg["To"] = TO

    msg["Subject"] = subject

    # html = """
    # This email is sent using <b>Python </b>!
    # """

    text = bs(html, "html.parser").text

    text_part = MIMEText(text, "plain")
    html_part = MIMEText(html, "html")

    msg.attach(text_part)
    msg.attach(html_part)
    #PUSH MAIL
    server = smtplib.SMTP("smtp.gmail.com", 587)

    server.starttls()

    server.login(email, password)

    server.sendmail(FROM, TO, msg.as_string())

    server.quit()



