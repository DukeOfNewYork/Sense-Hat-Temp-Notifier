import socket

from sense_emu import SenseHat

from senseemail import sendemail

sense = SenseHat()

msg = 'A simple test of the email protocol'

# The Sense Hat is accurate but normally a few degrees off, put a int here to compensate for that
offset = 0

# The temperature that the system sends an alert e-mail
alertTmp = 80

# these are the two display colors, highlight is the highlighted area and background is the background
primary = (0, 0, 255)
secondary = (0, 0, 0)
highlight = primary
background = secondary
# the array of display numbers repressing each number 0-9, the makeDisplay function turns each 1 to b and each 0 to e
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

gyroRoll = 0
displayArray = 0


# Pings a known local address to return a local IP address
def getip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # replace 127.0.0.1 with a known internal IP address
    s.connect(("127.0.0.1", 80))
    return (s.getsockname()[0])


# Takes a input temperature, uses this to get the 10's and 1's place, then uses each of those numbers to select a frame, then combines the frames using | (or) and outputs that.
def setdisplaybits(tmp):
    if tmp > 99:
        tmp = 99
    num = 0
    mulando = (tmp % 10)
    num = (frame[int((tmp - mulando) / 10)]) | (frame[mulando] >> 4)
    return num


# Takes the temperature of both the humidity sensor and the regular temprature sensore and averages them out then converts to Fahrenheit then adds the temprature offset variable.
def gettmp(tmpOffset=0):
    celsiusH = sense.get_temperature_from_humidity()
    celsiusP = sense.get_temperature_from_pressure()
    tempH = 9.0 / 5.0 * celsiusH + 32
    tempP = 9.0 / 5.0 * celsiusP + 32
    tempH = int(tempH)
    tempP = int(tempP)
    tempCombined = (tempP + tempH) / 2 + tmpOffset
    return int(tempCombined)


# takes both an array (the display array) then converts it from binary to a list of the variable e and b, which both contain color information, that the display can use.
def makedisplay(insBin):
    finalDisplay = []
    inBin = '{:064b}'.format(insBin)
    for x in range(0, 64):
        if inBin[x] == '0':
            finalDisplay.append(background)
        else:
            finalDisplay.append(highlight)
    return finalDisplay


def pixledisplay(currenttemp):
    displayarray = (setdisplaybits(currenttemp))
    sense.clear
    sense.set_pixels(makedisplay(displayarray))


# the e-mail statements are commented out so it will still run even if those values aren't configured.
while True:
    temp = gettmp()
    # msgReport combines the local IP and temprature info for easy e-mailing.
    msgReport = 'my IP address is ' + str(getip()) + ' and the temp is ' + str(temp)
    pixledisplay(temp)
    # This sends a e-mail if the temperature is above the alert temprature
    if (temp > alertTmp):
        sendemail(msgReport)
        while temp > alertTmp:
            temp = gettmp()
            highlight = (255, 0, 0)
            pixledisplay(temp)
    for event in sense.stick.get_events():
        print((event.action, event.direction))
        # When down is pressed it'll reset the color from the alert red
        if (event.action == 'pressed' and event.direction == 'down'):
            sense.show_message("Reset")
            highlight = primary
        elif (event.action == 'pressed' and event.direction == 'up'):
            sense.show_message(sendemail(msg))
        elif (event.action == 'pressed' and event.direction == 'middle'):
            sense.show_message(sendemail(msgReport))
