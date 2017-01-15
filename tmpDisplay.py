import pygame
import time
import socket
import math
import smtplib


from pygame.locals import *
from sense_emu import SenseHat
sense = SenseHat()

fromaddr = 'E-Mail Address that the message will be sent to'
toaddrs  = 'E-Mail Address that you want to alert'
msg = 'The Pimary Message'
msgTest = 'Message sent when pressing the Sense Hat stick down'
username = 'E-Mail UserName'
password = 'E-Mail Password'
server = smtplib.SMTP('SMTP address and port',587)

offset = #The Sense Hat is accurate but normaly a few degrees off, put a int here to compensate for that

pygame.init()
pygame.display.set_mode((640, 480))

running = True
alertTmp = 80

b = (0, 0, 255)
e = (0, 0, 0)

frame = [[b,b,b,e,e,e,e,e,b,e,b,e,e,e,e,e,b,e,b,e,e,e,e,e,b,e,b,e,e,e,e,e,b,b,b,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e],
[e,e,b,e,e,e,e,e,e,e,b,e,e,e,e,e,e,e,b,e,e,e,e,e,e,e,b,e,e,e,e,e,e,e,b,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e],
[b,b,b,e,e,e,e,e,e,e,b,e,e,e,e,e,b,b,b,e,e,e,e,e,b,e,e,e,e,e,e,e,b,b,b,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e],
[b,b,b,e,e,e,e,e,e,e,b,e,e,e,e,e,b,b,b,e,e,e,e,e,e,e,b,e,e,e,e,e,b,b,b,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e],
[b,e,b,e,e,e,e,e,b,e,b,e,e,e,e,e,b,b,b,e,e,e,e,e,e,e,b,e,e,e,e,e,e,e,b,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e],
[b,b,b,e,e,e,e,e,b,e,e,e,e,e,e,e,b,b,b,e,e,e,e,e,e,e,b,e,e,e,e,e,b,b,b,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e],
[b,b,b,e,e,e,e,e,b,e,e,e,e,e,e,e,b,b,b,e,e,e,e,e,b,e,b,e,e,e,e,e,b,b,b,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e],
[b,b,b,e,e,e,e,e,e,e,b,e,e,e,e,e,e,e,b,e,e,e,e,e,e,e,b,e,e,e,e,e,e,e,b,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e],
[b,b,b,e,e,e,e,e,b,e,b,e,e,e,e,e,b,b,b,e,e,e,e,e,b,e,b,e,e,e,e,e,b,b,b,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e],
[b,b,b,e,e,e,e,e,b,e,b,e,e,e,e,e,b,b,b,e,e,e,e,e,e,e,b,e,e,e,e,e,e,e,b,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e]]

def getTmp (pos, tmpOffset=offset):
    celsiusH = sense.get_temperature_from_humidity()
    celsiusP = sense.get_temperature_from_pressure()
    tempH = 9.0/5.0 * celsiusH + 32
    tempP = 9.0/5.0 * celsiusP + 32
    tempH = int(tempH)
    tempP = int(tempP)
    tempCombined = (tempP + tempH)/2-tmpOffset
    return tempCombined;
        
def setDisplay (tmp,pos):
    num=[]
    tmp = str(tmp)
    if pos == 0:
        num=frame[int(tmp[0])]
    elif pos == 1:
        for x in range(0,64):
            num.append(e)
        for y in range(0,60):
            if frame[int(tmp[1])][y]==b:
                num[y+4]=b
    else:
        num= 0
    return num;


while running:
    leftNum=[]
    rightNum=[]

    leftNum=setDisplay(getTmp(0),0)
    rightNum=setDisplay(getTmp(1),1)

                    
    sense.clear
    

    DisplayNum=[]
    for x in range(0,64):
     if leftNum[x]==b or rightNum[x]==b:
         DisplayNum.append(b)
     else:
         DisplayNum.append(e)
    sense.set_pixels(DisplayNum)
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            

            if event.key == K_DOWN:
                server.ehlo()
                server.starttls()
                server.login(username,password)
                server.sendmail(fromaddr, toaddrs, msgTest)
                server.quit()
               
            elif event.key == K_UP:
                x=x+x
            elif event.key == K_RIGHT:
                x=x+1
            elif event.key == K_LEFT:
                x=x+1
            elif event.key == K_RETURN:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("cravencc.edu",80))
                name=(s.getsockname()[0])
                sense.show_message(name,text_colour=[255,255,255])

                
                  

        
        if event.type == QUIT:
            running = False
            print("BYE")
