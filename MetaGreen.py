import pyautogui as pag
from comet_ml import Experiment
from time import sleep
import serial
import RPi.GPIO as gpio
import datetime as dt
import smtplib
from email.mime.text import MIMEText
from getpass import getpass
from moviepy.editor import *
import pygame
import notify2

gpio.setmode(gpio.BCM)
gpio.setup(16, gpio.OUT)

def send(t, m):
    notify2.init("test")
    n = notify2.Notification(t,m)
    n.show()
    return

def email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")
    
def mp4(vid):
    clip = VideoFileClip(vid).resize(0.5)
    clip.preview()
    pygame.quit() 

hr = 0
i = 0

# Your Comet API key, project name, and workspace
api_key = "P3nNsRHKruJCDu8I9oiWCiecx"
project_name = "metagreen"
workspace = "shadow-rhodium"

subject = "MetaGreen Notification"
sender = "sb10599@dnsalbarsha.com"
recipients = ["elemental.h.nasser@gmail.com", "Diana.mousa@dnsalbarsha.com"]
password = getpass("Password: ")

experiment = Experiment(api_key=api_key, project_name=project_name, workspace=workspace)

# Your condition for taking a screenshot

s = 0
try:
    ser = serial.Serial("/dev/ttyACM0") #COM can be found in Arduino IDE
    sleep(2)
except:
    print("Arduino not connected")

while True:  
    try:
        line = ser.readline().decode("utf-8") 
        lst = line.split()

    except:
        print("Arduino Disconnected")
        break

    try:
            CO2 = int(lst[0])
            light = int(lst[1])
            temperature = int(lst[2])
            humidity = int(lst[3])
            LDR = int(lst[4])
            moisture = int(lst[5])

            if moisture < 300:
                     print("HIGH Moisture")

            elif moisture > 300 and moisture < 950:
                     print("MID Moisture")

            else:
                     print("LOW Moisture")


            if CO2 > 800:
                print("HIGH CO2 Level Detected")

            if temperature > 35:
                gpio.output(16, gpio.HIGH)

            else:
                gpio.output(16, gpio.LOW)



            try:
                ir = int(lst[6])

                if ir in range(4500, 4600):
                    print("OFF")
                    break

                elif ir in range(4700,4800):
                    s=s+1
                    pag.screenshot(f"/home/kali/Pictures/scrn{s}.png")
                    print("screenshot taken!")

            except:
                ir = "no signal"

            OUT1 = f"CO2 Level:{CO2} // Moisture {moisture}"
            OUT2 = f"Brightness Level: {light} // LDR: {LDR}"
            DHT11 = f"Temperature: {temperature} C // Humidity: {humidity}"
            OUT3 = f"Remote: {ir}"

            print(OUT1)
            print(OUT2)
            print(DHT11)
            print(OUT3)

    except:
            print("waiting for input")

    x = dt.datetime.now()
    H = x.strftime("%H")

    if H!=hr:
        experiment = Experiment(api_key=api_key, project_name=project_name, workspace=workspace)

    # Capture a screenshot
        path = f"/home/kali/Pictures/pic{i}.png"
        screenshot = pag.screenshot()#,region=(0,0, 300, 400))
        screenshot.save(path)
        
        # Log the screenshot to Comet.ml
        experiment.log_image(path, name='Detected_Screenshot') # Add your metadata
        experiment.log_text(OUT1)
        experiment.log_text(OUT2)
        experiment.log_text(DHT11)
        experiment.log_text(OUT3)

        hr = H
        i=i+1

        email(subject, "Data Recorded", sender, recipients, password)
        send("MetaGreen","Data Recorded")
        mp4("Downloads/98.mp4")

    if i == 6:
        break

    # End the experiment
experiment.end()
    