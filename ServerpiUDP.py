# -*- coding: utf-8 -*- 
import socket
from threading import Thread
import threading
import time
import RPi.GPIO as GPIO          

in1 = 24
in2 = 23
en = 25
wh = 26
p1 = 12
p2 = 16

ssleep = 0.01

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.setup(wh,GPIO.OUT)
GPIO.setup(p1,GPIO.OUT)
GPIO.setup(p2,GPIO.OUT)

p=GPIO.PWM(en,1000)
p.start(50)

wpwm=GPIO.PWM(wh,50)
wpwm.start(7.6)

panxpwm=GPIO.PWM(p1,50)
panxpwm.start(7.5)

panypwm=GPIO.PWM(p2,50)
panypwm.start(7.5)

def Main():
    host = '192.168.43.189'
    port = 22000

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host,port))

    print("Server Started.")
    while True:
        data, addr = s.recvfrom(2048)
        print (data)

        veri = data.encode().split(":")
        global x1
        global x2
        global x3
        global x4

        x1 = veri[0]
        x2 = veri[1]
        x3 = veri[2]
        x4 = veri[3]

        thread1 = threading.Thread(target=dcmotor, args=(x1,))
        thread2 = threading.Thread(target=wheelservo, args=(x2,))
        thread3 = threading.Thread(target=panx, args=(x3,))
        thread4 = threading.Thread(target=pany, args=(x4,))

        thread1.start()
        thread2.start()
        thread3.start()
        thread4.start()   

    s.close()

def dcmotor(x1):
        
    if (int(x1) < 500):
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        p.ChangeDutyCycle((499 - int(x1))/8)
        #print ('Geri :' + str((499 - int(x1))/8))

    if (int(x1) > 524):
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        p.ChangeDutyCycle((int(x1) - 525)/8)
        #print ('İleri :' + str((int(x1) - 525)/8))
        
    if (int(x1) <= 524) and (int(x1) >= 500):
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        p.ChangeDutyCycle(0)
        #print ('Hareketsiz')

def wheelservo(x2):
    
    if (int(x2) < 500):

        wpwm.ChangeDutyCycle( ( ( 500.0 - float(x2) ) * 0.004 ) + 7.6 )
        #print( ( ( 500.0 - float(x2) ) * 0.0052 ) + 7.5 )
        time.sleep(ssleep)

    if (int(x2) > 520):

        wpwm.ChangeDutyCycle( 7.6 - ( ( float(x2) - 520.0 ) * 0.004 ) )
        #print( 7.5 - ( ( float(x2) - 520.0 ) * 0.0052 ) )
        time.sleep(ssleep)
    
    if (int(x2) < 520) and (int(x2) > 500):

        wpwm.ChangeDutyCycle(7.6)
        time.sleep(ssleep)
        #print x2

def panx(x3):
    
    if (int(x3) < 500):

        panxpwm.ChangeDutyCycle( ( ( 500.0 - float(x3) ) * 0.0052 ) + 7.5 )

    if (int(x3) > 520):

        panxpwm.ChangeDutyCycle( 7.5 - ( ( float(x3) - 520.0 ) * 0.0052 ) )
    
    if (int(x3) < 520) and (int(x3) > 500):

        panxpwm.ChangeDutyCycle(7.5)
    
def pany(x4):
    
    if (int(x4) < 500):

        panypwm.ChangeDutyCycle( 7.5 - ( ( 500.0 - float(x4) ) * 0.0062 ) )

    if (int(x4) > 520):

        panypwm.ChangeDutyCycle( 7.5 + ( ( float(x4) - 520.0 ) * 0.0062 ) )
    
    if (int(x4) < 520) and (int(x4) > 500):

        panypwm.ChangeDutyCycle(7.5)

if __name__ == '__main__':
    Main()