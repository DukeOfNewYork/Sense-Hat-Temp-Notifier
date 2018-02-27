import smtplib

# This sets if e-mails are sent or not
email_enable = False

# This is all web server setup, this has been speficially used with Gmail
# msg is the primary temprature alert message while msgTest is just a message sent when pressing down the control stick
fromaddr = 'E-Mail Address that the message will be sent to'
toaddrs = 'E-Mail Address that you want to alert'
username = 'E-Mail UserName'
password = 'E-Mail Password'
mailserver = 'SMTP address and port'


# This works with Gmail but may need to be adjusted for other e-mail salutions

def sendemail(emailMessage):
    if email_enable:
        try:
            server = smtplib.SMTP(mailserver)
            server.ehlo()
            server.starttls()
            server.login(username, password)
            server.sendmail(fromaddr, toaddrs, emailMessage)
            server.quit()
            return ("Sent")
        except Exception as exc:
            return ("X " + str(exc))
    else:
        return ("Disabled")
