import imaplib
import email
from email.header import decode_header
import webbrowser
import os



passAndCommand = []

def getMail(username, password, N):
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    # authenticate
    imap.login(username, password)
    # https://myaccount.google.com/u/8/lesssecureapps?pli=1&rapt=AEjHL4NJd3IiGHuBFb0-dA_SOEtAbQo-JG-RIlsW3m0LQ2gX1952HXuv30AefeBbmc6xbNzXqWPZJerqo8a3fkPtTIxu-5dl9A
    status, messages = imap.select("INBOX")
    # number of top emails to fetch
    #N = 1
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
                #print("Subject:", subject)
                #print("From:", From)
                try:
                    temp_string = From.split()
                    temp_string1 = temp_string[2]
                    temp_string2 = temp_string1[1:]
                    temp_string3 = temp_string2.rstrip(temp_string2[-1])
                    passAndCommand.append(temp_string3)

                    passAndCommand.append(subject)
                except Exception as e:
                    print(e)
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
                            #print("Body:", body)
                            org_string = body
                            size = len(org_string)
                            mod_string = org_string[:size - 2]
                            passAndCommand.append(mod_string)
                else:
                    # extract content type of email
                    content_type = msg.get_content_type()
                    # get the email body
                    body = msg.get_payload(decode=True).decode()
                    if content_type == "text/plain":
                        #print(body)
                        pass
                #print("_" * 150)
    imap.close()
    imap.logout()


