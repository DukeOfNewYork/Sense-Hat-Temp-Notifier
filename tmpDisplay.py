import time
import socket
import math
import smtplib

from sense_emu import SenseHat

sense = SenseHat()

msg = 'A simple test of the email protocol'

# The Sense Hat is accurate but normaly a few degrees off, put a int here to compensate for that
offset = 0

#The temprature that the system sends an alert e-mail
alertTmp = 80

# these are the two display colors, b is the number and e is the background
b = (0, 0, 255)
e = (0, 0, 0)
# the array of display numbers represting each number 0-9, the makeDisplay function turns each 1 to b and each 0 to e
frame = [0B1110000010100000101000001010000011100000000000000000000000000000,
         0B0010000000100000001000000010000000100000000000000000000000000000,
         0B1110000000100000111000001000000011100000000000000000000000000000,
         0B1110000000100000111000000010000011100000000000000000000000000000,
         0B1010000010100000111000000010000000100000000000000000000000000000,
         0B1110000010000000111000000010000011100000000000000000000000000000,
         0B1110000010000000111000001010000011100000000000000000000000000000,
         0B1110000000100000001000000010000000100000000000000000000000000000,
         0B1110000010100000111000001010000011100000000000000000000000000000,
         0B1110000010100000111000000010000000100000000000000000000000000000]



running = True
gyroRoll = 0
displayArray = 0

# This is all web server setup, this has been speficially used with Gmail
# msg is the primary temprature alert message while msgTest is just a message sent when pressing down the control stick
# fromaddr = 'E-Mail Address that the message will be sent to'
# toaddrs  = 'E-Mail Address that you want to alert'
# username = 'E-Mail UserName'
# password = 'E-Mail Password'
# server = smtplib.SMTP('SMTP address and port',587)

# This works with Gmail but may need to be adjusted for other e-mail salutions
#def sendemail(accountName, accountPassword, emailFromAdress, emailToAdresss, emailMessage):
#    server.ehlo()
#    server.starttls()
#    server.login(accountName, accountPassword)
#    server.sendmail(emailFromAdress, emailToAdresss, emailMessage)
#    server.quit()


# Pings a known local address to return a local IP address
def getip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("known internal IP address", 80))
    return (s.getsockname()[0])


# Takes a input temprature, uses this to get the 10's and 1's place, then uses each of those numbers to select a frame, then combines the frames using | (or) and outputs that.
def setdisplaybits(tmp):
    if tmp > 99:
        tmp = 99
    num = 0
    mulando = (tmp % 10)
    num = (frame[int((tmp - mulando) / 10)]) | (frame[mulando] >> 4)
    return num


def gettmp(tmpOffset=0):
    celsiusH = sense.get_temperature_from_humidity()
    celsiusP = sense.get_temperature_from_pressure()
    tempH = 9.0 / 5.0 * celsiusH + 32
    tempP = 9.0 / 5.0 * celsiusP + 32
    tempH = int(tempH)
    tempP = int(tempP)
    tempCombined = (tempP + tempH) / 2 - tmpOffset
    return int(tempCombined)


def makedisplay(insBin):
    finalDisplay = []
    inBin = '{:064b}'.format(insBin)
    for x in range(0, 64):
        if inBin[x] == '0':
            finalDisplay.append(e)
        else:
            finalDisplay.append(b)
    return finalDisplay


while running:
    temp = gettmp()
    displayarray = (setdisplaybits(temp))
    sense.clear
    sense.set_pixels(makedisplay(displayarray))
    for event in sense.stick.get_events():
        print((event.action, event.direction))
#        if (event.action == 'pressed' and event.direction == 'up'):
#            sendemail(username, password, username, toaddrs, msg)
        elif (event.action == 'pressed' and event.direction == 'down'):
            sense.show_message(temp)
#        elif (event.action == 'pressed' and event.direction == 'middle'):
#            msgReport = 'my IP address is ' + str(getip()) + ' and the temp is ' + str(temp)
#            sendemail(username, password, username, toaddrs, msgReport)
