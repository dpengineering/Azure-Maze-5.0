import datetime
import imaplib
import email
import random
from email.header import decode_header
import webbrowser
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from bs4 import BeautifulSoup as bs
from threading import Thread
import time


class Email:
    temp_subject = " "
    providers = ['@txt.att.net', '@tmomail.net', '@vtext.com']
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_info(self):
        return self.username, self.password

    def checkForEmail(self, target_body=None, response_subject=None, response_body=None, returnable=False):
        current_mail = self.getMail()
        sender = current_mail[0]
        sender_subject = current_mail[1]
        sender_body = current_mail[2]

        if target_body in sender_body.lower() and sender_subject.lower() != self.temp_subject:
            if returnable:
                return True
            else:
                self.sendMail(sender, response_subject, response_body)
                self.sendMail(self.username, response_subject + str(random.random()), response_body)
                self.temp_subject = sender_subject.lower()

    def sendMail(self, TO, subject, body):
        FROM = self.username

        msg = MIMEMultipart("alternative")

        msg["From"] = FROM

        msg["To"] = TO

        msg["Subject"] = subject

        text = bs(body, "html.parser").text

        text_part = MIMEText(text, "plain")
        html_part = MIMEText(body, "html")

        msg.attach(text_part)
        msg.attach(html_part)

        # PUSH MAIL
        server = smtplib.SMTP("smtp.gmail.com", 587)

        server.starttls()

        server.login(self.username, self.password)

        server.sendmail(FROM, TO, msg.as_string())

        server.quit()

    def getMail(self, N=1):
        mailArray = []
        imap = imaplib.IMAP4_SSL("imap.gmail.com")
        # authenticate
        imap.login(self.username, self.password)
        # https://myaccount.google.com/u/8/lesssecureapps?pli=1&rapt=AEjHL4NJd3IiGHuBFb0-dA_SOEtAbQo-JG-RIlsW3m0LQ2gX1952HXuv30AefeBbmc6xbNzXqWPZJerqo8a3fkPtTIxu-5dl9A
        status, messages = imap.select("INBOX")
        # number of top emails to fetch
        # N = 1
        # total number of emails
        messages = int(messages[0])

        for i in range(messages, messages - N, -1):
            # fetch the email message by ID
            res, msg = imap.fetch(str(i), "(RFC822)")
            for response in msg:
                if isinstance(response, tuple):
                    # parse a bytes email into a message object
                    msg = email.message_from_bytes(response[1])
                    # decode the email subject
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        # if it's a bytes, decode to str
                        subject = subject.decode(encoding)
                    # decode email sender
                    From, encoding = decode_header(msg.get("From"))[0]
                    if isinstance(From, bytes):
                        From = From.decode(encoding)
                    # print("Subject:", subject)
                    # print("From:", From)
                    try:
                        temp_string = From.split()
                        temp_string1 = temp_string[2]
                        temp_string2 = temp_string1[1:]
                        temp_string3 = temp_string2.rstrip(temp_string2[-1])
                        mailArray.append(temp_string3)

                        mailArray.append(subject)
                    except Exception as e:
                        pass
                    # if the email message is multipart
                    if msg.is_multipart():
                        # iterate over email parts
                        for part in msg.walk():
                            # extract content type of email
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            try:
                                # get the email body
                                body = part.get_payload(decode=True).decode()

                            except Exception as e:
                                # print(e)
                                pass
                            if content_type == "text/plain" and "attachment" not in content_disposition:
                                # print text/plain emails and skip attachments
                                # print("Body:", body)
                                org_string = body
                                size = len(org_string)
                                mod_string = org_string[:size - 2]
                                mailArray.append(mod_string)
                    else:
                        # extract content type of email
                        content_type = msg.get_content_type()
                        # get the email body
                        body = msg.get_payload(decode=True).decode()
                        if content_type == "text/plain":
                            # print(body)
                            pass
                    # print("_" * 150)
        imap.close()
        imap.logout()
        return mailArray

    email_array = []

    def checkForEmailConstantly(self, target_body=None, response_subject=None, response_body=None, returnable=False):
        self.email_array.append(target_body)
        self.email_array.append(response_subject)
        self.email_array.append(response_body)
        self.email_array.append(returnable)
        time.sleep(0.5)
        Thread(target=self.checkForEmailBotThread).start()

    def checkForEmailBotThread(self):

        target_body = self.email_array[0]
        response_subject = self.email_array[1]
        response_body = self.email_array[2]
        returnable = self.email_array[3]

        while True:
            try:
                current_mail = self.getMail()
                sender = current_mail[0]
                sender_subject = current_mail[1]
                sender_body = current_mail[2]

                if target_body in sender_body.lower() and sender_subject.lower() != self.temp_subject:
                    if returnable:
                        return True
                    else:
                        self.sendMail(sender, response_subject, response_body)
                        self.sendMail(self.username, response_subject + str(random.random()), response_body)
                        self.temp_subject = sender_subject.lower()
                        print(f'sent message {response_subject} to {sender} on {datetime.datetime.now()}')
            except Exception as e:
                pass







