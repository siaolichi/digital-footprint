
import random
import time
from datetime import datetime
import requests
import hashlib
import cv2
import os
import socket
from ssh2.session import Session
from pythonosc import udp_client
# OSC Config
osc_port = 5005
osc_ip = '127.0.0.1'
client = udp_client.SimpleUDPClient(osc_ip, osc_port)
# Static varialble
database = []
status = 0
data_id = 0
# OpenCV Config
path = os.path.dirname(os.path.abspath(__file__))
cam = cv2.VideoCapture(0)
detector=cv2.CascadeClassifier(path+r'/Classifiers/face.xml')
time.sleep(2)
# ssh2 Config
rasp_host = '192.168.11.8'
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((rasp_host, 22))
session = Session()
session.handshake(sock)
session.userauth_password('pi', '12345678')

def generateHash(data_id):
  now = datetime.now()
  time = str(datetime.now().isoformat(' ', 'seconds'))
  name = hashlib.sha224(str.encode( str(data_id) + time )).hexdigest()
  database.append({id: id, name: name})
  client.send_message("/lyric", "ID number, " + str(data_id) + ", Time, " + time)
  return name

def printHashCode(code):
  channel = session.open_session()
  # channel.execute('sudo python3 /home/pi/python/printer.py "' + code + '"')
  channel.close()


if __name__ == "__main__":
  while True:
    ret, im =cam.read()
    gray=cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    faces=detector.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(100, 100), flags=cv2.CASCADE_SCALE_IMAGE)
    print(len(faces))
    for(x,y,w,h) in faces:

      if(status == 1):
        # generate hash code and send data to TD
        name = generateHash(data_id)
        # save image with hash code
        cv2.imwrite("dataSet/"+name+".jpg", im)
        printHashCode(name)
        print("sent!")
        data_id += 1

      cv2.rectangle(im,(x-50,y-50),(x+w+50,y+h+50),(225,0,0),2)
      status = 0
    if len(faces) == 0:
      print('no face detected')
      status = 1
    cv2.waitKey(50)
    cv2.imshow('im',im)