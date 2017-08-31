import smtplib

    #This is all web server setup, this has been speficially used with Gmail
    #msg is the primary temprature alert message while msgTest is just a message sent when pressing down the control stick
#fromaddr = 'E-Mail Address that the message will be sent to'
#toaddrs  = 'E-Mail Address that you want to alert'
#username = 'E-Mail UserName'
#password = 'E-Mail Password'
#server = smtplib.SMTP('SMTP address and port',587)

# This works with Gmail but may need to be adjusted for other e-mail salutions

def sendemail(emailMessage):
    server.ehlo()
    server.starttls()
    server.login(username, password)
    server.sendmail(fromaddr, toaddrs, emailMessage)
    server.quit()

