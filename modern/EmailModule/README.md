# EmailModule
Quick and easy read and response, True/False returning, Checks and responds to Emails.


## How to Use
On a basic level, you really just need to use 
```
from EmailModule import checkforEmail

checkforEmail(username, password, targetbody, responsesubject, responsebody, bool)
```


###### Username is your gmail username, password is your gmail password, pretty simple. this function takes the message, or the 'body' of the email, and converts it to all lowercase. If it contains 'targetbody' then it will respond with 'responsesubject' and 'responsebody'. If you want this function to execute only once after it receives the correct 'targetbody', then make bool True. If you want a continous checker/responder, then make bool False.

> I reccommend that you use an entirely new gmail account as you need to:
https://myaccount.google.com/u/8/lesssecureapps?pli=1&rapt=AEjHL4NJd3IiGHuBFb0-dA_SOEtAbQo-JG-RIlsW3m0LQ2gX1952HXuv30AefeBbmc6xbNzXqWPZJerqo8a3fkPtTIxu-5dl9A


`Look here for Initial Sources:` [Reading Emails with Python](https://www.thepythoncode.com/article/reading-emails-in-python) | 
[imaplib — IMAP4 protocol client](https://docs.python.org/3/library/imaplib.html) | 
[email — An email and MIME handling package](https://docs.python.org/3/library/email.html) | 
[webbrowser — Web-browser controller](https://docs.python.org/3/library/webbrowser.html)
