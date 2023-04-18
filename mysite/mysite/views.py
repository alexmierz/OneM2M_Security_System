from django.shortcuts import render, redirect

#import socket


import os.path
#import PIL.Image #pip install Pillow
import io
import base64
import urllib.parse
#from rdflib import Graph

# for reading configuration parameters from file
import argparse
from configparser import ConfigParser

# for sending http requests using json
import requests
from json import loads, dumps

# the sensors and http listener (for notifications) use threads
#import threading
#import time
from http.server import HTTPServer, BaseHTTPRequestHandler


def status(request):
    return render(request, 'templates/status.html')

#configFile = "./lamppost-F1.cfg"
configFile = os.path.join(os.path.dirname(__file__), 'lamppost-F1.cfg')


#Reading Configuration Details
parser = ConfigParser()
parser.optionxform = str
parser.read(configFile)
appIP = parser.get('CONFIG_DATA', 'appIP')
appPort = int(parser.get('CONFIG_DATA', 'appPort'))
appID = parser.get("CONFIG_DATA", "appID")
cseIP = parser.get('CONFIG_DATA', 'cseIP')
csePort = parser.get('CONFIG_DATA', 'csePort')
cseID = parser.get('CONFIG_DATA', 'cseID')
cseName = parser.get('CONFIG_DATA', 'cseName')




deviceName = parser.get("DEVICE_CONFIG", "deviceName")
Illuminance = parser.get("DEVICE_CONFIG", "Illuminance")
Luminescence = parser.get("DEVICE_CONFIG", "Luminescence")
Phosphorescence = parser.get("DEVICE_CONFIG", "Phosphorescence")
LightAbsorption = parser.get("DEVICE_CONFIG", "LightAbsorption")
Lamp1 = parser.get("DEVICE_CONFIG", "Lamp")
Lamp_ON = parser.get("DEVICE_CONFIG", "Lamp_On")
Lamp_OFF = parser.get("DEVICE_CONFIG", "Lamp_Off")
X_position = parser.get("DEVICE_CONFIG", "X_position")
Y_position = parser.get("DEVICE_CONFIG", "Y_position")
REGISTER_ON_START = parser.get("DEVICE_CONFIG", "REGISTER_ON_START")
DEREGISTER_ON_EXIT = parser.get("DEVICE_CONFIG", "DEREGISTER_ON_EXIT")



def home(request):

        poa = 'http://{}:{}'.format(appIP,appPort)
        payld = { "m2m:ae": { "rr": True, "api": "NR_AE001", "apn": "IOTApp", "csz": [ "application/json" ], "srv": [ "2a" ], "rn": deviceName, "poa": [ poa ]} }
        
        print ("AE Create Request")
        #print (payld)
        #url = 'http://' + cseIP + ':' + csePort + '/' + cseID
        url = 'http://35.89.20.163:8080/psu23-capstone'
        hdrs = {'X-M2M-RI':"CAE_Test",'X-M2M-Origin':appID, 'X-M2M-RVI':'2a' ,'Content-Type':"application/json;ty=2"}
        r = requests.post(url, data=dumps(payld), headers=hdrs)
        print ("AE Create Response")
        print (r.text)

        payld = {"m2m:acp" :{"rn": "CF1-ACP", "pv": {"acr": [{"acor":["CF1"], "acop": 63}]},"pvs": {"acr": [{"acor":["CF1"], "acop": 63},{"acor":["CF1"], "acop": 63}]}}}
        print("Make ACP")
        #url = 'http://' + cseIP + ':' + csePort + '/' + parentID
        url = 'http://35.89.20.163:8080/psu23-cse/lamppost-F1'
        hdrs = {'X-M2M-RI':"CAE_Test",'X-M2M-Origin':"CF1", 'X-M2M-RVI':'2a' ,'Content-Type':"application/json;ty=1"}
        r = requests.post(url, data=dumps(payld), headers=hdrs)
        print("ACP CReate REsponse")
        print(r.text)

       # return getResId('m2m:ae',r)
        #print("sent?")
        return render(request, "home.html", {})


def garage(request):
    return render(request, "garage.html")
#10
def create(request):
    payld = { "m2m:cnt": { "rn": "thingy91", "lbl": [ "key1", "key2" ], "mni": 10,  "acpi": ["psu23-cse/lamppost-F1/CF1-ACP"]} }
    print ("CNT Create Request")
    #print (payld)
    #url = 'http://' + cseIP + ':' + csePort + '/' + "lamppost-F1"
    url = 'http://35.89.20.163:8080/psu23-cse/lamppost-F1'
    hdrs = {'X-M2M-RI':"CAE_Test",'X-M2M-Origin': "CF1", 'X-M2M-RVI':'2a' ,'Content-Type':"application/json;ty=3"}
    r = requests.post(url, data=dumps(payld), headers=hdrs)
    print ("CNT Create Response")
    print (r.text)
    


    payld = { "m2m:cin": { "cnf": "application/text:0", "con": "1"} }
    print ("CI Create Request")
    #print (payld)
    #url = 'http://' + cseIP + ':' + csePort + '/' + parentID
    url = 'http://35.89.20.163:8080/psu23-cse/lamppost-F1/thingy91'
    hdrs = {'X-M2M-RI':"sensorValue",'X-M2M-Origin':"CF1", 'X-M2M-RVI':'2a' ,'Content-Type':"application/json;ty=4"}
    r = requests.post(url, data=dumps(payld), headers=hdrs)
    print ("CIN Create Response")
    print (r.text)
    url = 'http://35.89.20.163:8080/psu23-cse/lamppost-F1/thingy91/la'
    hdrs = {'X-M2M-RI':"CAE_Test",'X-M2M-Origin': "CF1", 'X-M2M-RVI':'2a' ,'Accept':"application/json"}
    r = requests.get(url, data=dumps(payld), headers=hdrs)
    print(r.text[50])
    #cont = int(r.text[50])
    text = str(r.text)
    start = text.find('"con":')
    print(start)
    cont = int(r.text[start + 8])

    #return getResId('m2m:cnt',r)
    return render(request, "status.html", {"cont": cont})
    #psu23-cse/lamppost-F1/thingy91



def status(request):
    return render(request, "status.html")

def upload(request):
    return render(request, "upload.html")

def temp(request):
    #url = 'http://' + cseIP + ':' + csePort + '/' + cseName + '/'+ resourceName
    url = 'http://35.89.20.163:8080/psu23-capstone/lamppost-F1'
    hdrs = {'X-M2M-RI':"CAE_Test",'X-M2M-Origin':"CF1", 'X-M2M-RVI':'2a' ,'Content-Type':"application/json"}
    r = requests.delete(url,  headers=hdrs)
    print ("AE Delete Response")
    print (r.text)
    return render(request, "temp.html")
    
    