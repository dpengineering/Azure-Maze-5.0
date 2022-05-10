import GetEmail
from GetEmail import getMail
from SendMail import sendMail
from time import sleep

def checkforEmail(username, password, targetbody, responsesubject, responsebody, bool):
    subject = ' '
    while True:
        getMail(username, password, 1)
        sleep(1)
        try:
            if targetbody in GetEmail.passAndCommand[2].lower() and GetEmail.passAndCommand[1] != subject:
                sendMail(username, password, str(GetEmail.passAndCommand[0]), responsesubject, responsebody)
                print('sent response', responsesubject + ',\n' + responsebody, 'to', GetEmail.passAndCommand[0], '\ntarget=', targetbody)
                subject = GetEmail.passAndCommand[1]
                if bool == True:
                    return True
                else:
                    pass
            else:
                pass
        except Exception as e:
            print(e, 'in checkforEmail')
        GetEmail.passAndCommand.clear()




