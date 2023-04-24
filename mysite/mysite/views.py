from django.shortcuts import render
import os.path
from configparser import ConfigParser
import requests
from json import dumps

# Setting the configuration path
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




def home(request):

        # create an AE resource -> Lamppost -F1
        poa = 'http://{}:{}'.format(appIP,appPort)
        payld = { "m2m:ae": { "rr": True, "api": "NR_AE001", "apn": "IOTApp", "csz": [ "application/json" ], "srv": [ "2a" ], "rn": deviceName, "poa": [ poa ]} }
        url = 'http://35.89.20.163:8080/psu23-capstone'
        hdrs = {'X-M2M-RI':"CAE_Test",'X-M2M-Origin':appID, 'X-M2M-RVI':'2a' ,'Content-Type':"application/json;ty=2"}
        r = requests.post(url, data=dumps(payld), headers=hdrs)
       
        print ("AE Create Response lamppost")
        print (r.text)

        # create an AE resource -> ThingyHex
        poa = 'http://{}:{}'.format(appIP,appPort)
        payld = { "m2m:ae": { "rr": True, "api": "NR_AE001", "apn": "IOTApp", "csz": [ "application/json" ], "srv": [ "2a" ], "rn": "ThingyHex", "poa": [ poa ]} }
        url = 'http://35.89.20.163:8080/psu23-capstone'
        hdrs = {'X-M2M-RI':"CAE",'X-M2M-Origin': "CF2", 'X-M2M-RVI':'2a' ,'Content-Type':"application/json;ty=2"}
        r = requests.post(url, data=dumps(payld), headers=hdrs)

        print ("AE Create Response Thingy")
        print (r.text)

        # create an ACP -> CF-1-ACP
        payld = {"m2m:acp" :{"rn": "CF1-ACP", "pv": {"acr": [{"acor":["CF1"], "acop": 63}]},"pvs": {"acr": [{"acor":["CF1"], "acop": 63},{"acor":["CF1"], "acop": 63}]}}}
        print("Make ACP for CF1")
        url = 'http://35.89.20.163:8080/psu23-cse/lamppost-F1'
        hdrs = {'X-M2M-RI':"CAE_Test",'X-M2M-Origin':"CF1", 'X-M2M-RVI':'2a' ,'Content-Type':"application/json;ty=1"}
        r = requests.post(url, data=dumps(payld), headers=hdrs)
        
        print("ACP CReate Response for CF1")
        print(r.text)

         # create an ACP -> CF-2-ACP
        payld = {"m2m:acp" :{"rn": "CF1-ACP", "pv": {"acr": [{"acor":["CF2"], "acop": 63}]},"pvs": {"acr": [{"acor":["CF2"], "acop": 63},{"acor":["CF2"], "acop": 63}]}}}
        print("Make ACP for CF2")
        url = 'http://35.89.20.163:8080/psu23-cse/ThingyHex'
        hdrs = {'X-M2M-RI':"CAE_Test",'X-M2M-Origin':"CF2", 'X-M2M-RVI':'2a' ,'Content-Type':"application/json;ty=1"}
        r = requests.post(url, data=dumps(payld), headers=hdrs)
        
        print("ACP CReate REsponse for CF2")
        print(r.text)



        # create a Container -> thingy91
        payld = { "m2m:cnt": { "rn": "thingy91", "lbl": [ "key1", "key2" ], "mni": 10,  "acpi": ["psu23-cse/lamppost-F1/CF1-ACP"]} }
        print ("CNT Create Request")
        #print (payld)
        #url = 'http://' + cseIP + ':' + csePort + '/' + "lamppost-F1"
        url = 'http://35.89.20.163:8080/psu23-cse/lamppost-F1'
        hdrs = {'X-M2M-RI':"CAE_Test",'X-M2M-Origin': "CF1", 'X-M2M-RVI':'2a' ,'Content-Type':"application/json;ty=3"}
        r = requests.post(url, data=dumps(payld), headers=hdrs)
        print ("CNT Create Response")
        print (r.text) 

        
        # create a Container -> raspberrypi
        payld = { "m2m:cnt": { "rn": "raspberrypi", "lbl": [ "key1", "key2" ], "mni": 10,  "acpi": ["psu23-cse/lamppost-F1/CF1-ACP"]} }
        print ("CNT Create Request")
        #print (payld)
        #url = 'http://' + cseIP + ':' + csePort + '/' + "lamppost-F1"
        url = 'http://35.89.20.163:8080/psu23-cse/lamppost-F1'
        hdrs = {'X-M2M-RI':"CAE_Test",'X-M2M-Origin': "CF1", 'X-M2M-RVI':'2a' ,'Content-Type':"application/json;ty=3"}
        r = requests.post(url, data=dumps(payld), headers=hdrs)
        print ("CNT Create Response")
        print (r.text) 
        
         # create a Container -> thingy91
        payld = { "m2m:cnt": { "rn": "thingy91", "lbl": [ "key1", "key2" ], "mni": 10,  "acpi": ["psu23-cse/ThingyHex/CF1-ACP"]} }
        print ("CNT Create Request")
        #print (payld)
        #url = 'http://' + cseIP + ':' + csePort + '/' + "lamppost-F1"
        url = 'http://35.89.20.163:8080/psu23-cse/ThingyHex'
        hdrs = {'X-M2M-RI':"CAE_Test",'X-M2M-Origin': "CF2", 'X-M2M-RVI':'2a' ,'Content-Type':"application/json;ty=3"}
        r = requests.post(url, data=dumps(payld), headers=hdrs)
        print ("CNT Create Response")
        print (r.text) 

        return render(request, "home.html", {})


def garage(request):
    return render(request, "garage.html")
#10
def status(request):

    # create a content instance
    payld = { "m2m:cin": { "cnf": "application/text:0", "con": "1"} }
    url = 'http://35.89.20.163:8080/psu23-cse/lamppost-F1/thingy91'
    hdrs = {'X-M2M-RI':"sensorValue",'X-M2M-Origin':"CF1", 'X-M2M-RVI':'2a' ,'Content-Type':"application/json;ty=4"}
    r = requests.post(url, data=dumps(payld), headers=hdrs)
    
    print ("CIN Create Response")
    print (r.text)

    # retrieve the contents of the latest content instance in the container
    url = 'http://35.89.20.163:8080/psu23-cse/lamppost-F1/thingy91/la'
    hdrs = {'X-M2M-RI':"CAE_Test",'X-M2M-Origin': "CF1", 'X-M2M-RVI':'2a' ,'Accept':"application/json"}
    r = requests.get(url, data=dumps(payld), headers=hdrs)

    # gets the status indicator
    text = str(r.text)
    start = text.find('"con":')
    cont = int(r.text[start + 8])


    return render(request, "status.html", {"cont": cont})



def upload(request):
    return render(request, "upload.html")



