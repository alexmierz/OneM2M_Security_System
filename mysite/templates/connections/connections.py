#import PySimpleGUI as sg  #pip install PySimpleGUI and sudo apt-get install python3-tk

# When a light button is pushed and the confirmation that the primitive is successful
# the icon will be changed. These imports support that functionality.
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


# Get the config filename from the commandline or default
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-c", "--config", type=str, default='device.cfg', help="Config file name")
args = parser.parse_args()
configFile = args.config



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


# These are <semanticdescriptor> payloads read from the config file
smdAEPayld = parser.get('DEVICE_CONFIG', 'smdAEPayld')
smdLightCommandPayld = parser.get('DEVICE_CONFIG', 'smdLightCommandPayld')
smdLightStatusPayld = parser.get('DEVICE_CONFIG', 'smdLightStatusPayld')
smdSensorPayld = parser.get('DEVICE_CONFIG', 'smdSensorPayld')

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

# AE-ID for this device
originator = appID
lamp1State = Lamp_OFF
# init these to empty values so that a <cin> will not be created 
# until the parent <container> is created
cntLtStatus = ""
cntLtA = ""
cntPho = ""
cntLum = ""
cntIll = ""

# handler for notifications. This method will first send a response to the notification
# back to the CSE. 
# This handler is ONLY able to process a notification of a <CIN> as that is 
# what is subscribed to.  It can be extended for notifications of other types of resources.
# The only subscription used is for the lampCommand, so the payload is sent to 
# a "-Lamp-" event handler 
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
        
    count = 0
    def do_POST(self):
        # Construct return header
        mySendResponse(self, 200, 2001)

        # Get headers and content data
        length = int(self.headers['Content-Length'])
        contentType = self.headers['Content-Type']
        post_data = self.rfile.read(length)
        
        # Print the content data
        print('### Notification')
        print (self.headers)
        print(post_data.decode('utf-8'))
        r = loads(post_data.decode('utf8').replace("'", '"'))
        lampCommand = r['m2m:sgn']['nev']['rep']['m2m:cin']['con']
        print(lampCommand)
        #window.write_event_value("-Lamp-", lampCommand)
        self.count += 1 # reduce the number of notifications printed in the console.
        if (self.count % 100 == 0):
          print("Not " + str(self.count))
              

def mySendResponse(self, responseCode, rsc, payload=None):
        self.send_response(responseCode)
        self.send_header("X-M2M-RI", self.headers['X-M2M-RI'])
        self.send_header("X-M2M-RSC", rsc)
        self.end_headers()
        if payload:
            self.wfile.write(payload.getvalue())
        
# To Do - refactor to a single function with a second parameter
# document purpose
def sensor_update(window):
    i=0
    while True:
        time.sleep(5)
        window.write_event_value("-Phosphorescence-", i)
        i += 1

def lamp_update(window):
    i=0
    while True:
        time.sleep(5)
        window.write_event_value("-Lamp-", i)
        i += 1

def lamp_command(window):
    httpd = HTTPServer(('', appPort), SimpleHTTPRequestHandler)
    print('**starting server & waiting for connections**')
    httpd.serve_forever()


# From https://pysimplegui.readthedocs.io/en/latest/cookbook/#the-pysimplegui-cookbook
# Recipe - Collapsible Sections (Visible / Invisible Elements)
def collapse(layout, key):
    """
    Helper function that creates a Column that can be later made hidden, thus appearing "collapsed"
    :param layout: The layout for the section
    :param key: Key used to make this seciton visible / invisible
    :return: A pinned column that can be placed directly into your layout
    :rtype: sg.pin
    """
    return sg.pin(sg.Column(layout, key=key))

# From https://pysimplegui.readthedocs.io/en/latest/cookbook/#the-pysimplegui-cookbook
# Recipe - convert_to_bytes Function + PIL Image Viewer
def convert_to_bytes(file_or_bytes, resize=None):
    '''
    Will convert into bytes and optionally resize an image that is a file or a base64 bytes object.
    Turns into  PNG format in the process so that can be displayed by tkinter
    :param file_or_bytes: either a string filename or a bytes base64 image object
    :type file_or_bytes:  (Union[str, bytes])
    :param resize:  optional new size
    :type resize: (Tuple[int, int] or None)
    :return: (bytes) a byte-string object
    :rtype: (bytes)
    '''
    if isinstance(file_or_bytes, str):
        img = PIL.Image.open(file_or_bytes)
    else:
        try:
            img = PIL.Image.open(io.BytesIO(base64.b64decode(file_or_bytes)))
        except Exception as e:
            dataBytesIO = io.BytesIO(file_or_bytes)
            img = PIL.Image.open(dataBytesIO)

    cur_width, cur_height = img.size
    if resize:
        new_width, new_height = resize
        scale = min(new_height/cur_height, new_width/cur_width)
        img = img.resize((int(cur_width*scale), int(cur_height*scale)), PIL.Image.ANTIALIAS)
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    del img
    return bio.getvalue()

# method to extract Resource Id from a CREATE primitive RESPONSE from the CSE
# tag is the resource type element in the json payload, e.g. 'm2m:ae'
# if the resource id is NOT PRESENT, this indicates that the resource already exists
# this could be checked by the response code instead of looking at the payload.
def getResId(tag,r):
    try:
        resId = r.json()[tag]['ri']
    except:
        #allready created
        resId = ""
    return resId

# the 'api' parameter is required, but not used for anything in the current use case. It does not
# have to be unique.
def createAE(resourceName):
    poa = 'http://{}:{}'.format(appIP,appPort)
    payld = { "m2m:ae": { "rr": True, "api": "NR_AE001", "apn": "IOTApp", "csz": [ "application/json" ], "srv": [ "2a" ], "rn": resourceName, "poa": [ poa ],"acpi": ["cse-in/acpLightAppPolicy"] } }
    
    print ("AE Create Request")
    #print (payld)
    url = 'http://' + cseIP + ':' + csePort + '/' + cseID
    hdrs = {'X-M2M-RI':"CAE_Test",'X-M2M-Origin':originator, 'X-M2M-RVI':'2a' ,'Content-Type':"application/json;ty=2"}
    r = requests.post(url, data=dumps(payld), headers=hdrs)
    print ("AE Create Response")
    print (r.text)

    return getResId('m2m:ae',r)

# This will delete all child resources, making this a good way to soft reset the scenario
def deleteAE(resourceName):
    url = 'http://' + cseIP + ':' + csePort + '/' + cseName + '/'+ resourceName
    hdrs = {'X-M2M-RI':"CAE_Test",'X-M2M-Origin':originator, 'X-M2M-RVI':'2a' ,'Content-Type':"application/json"}
    r = requests.delete(url,  headers=hdrs)
    print ("AE Delete Response")
    print (r.text)

def createContainer(resourceName, parentID, mni = 10):
    payld = { "m2m:cnt": { "rn": resourceName, "lbl": [ "key1", "key2" ], "mni":mni,"acpi": ["cse-in/acpLightAppPolicy"]} }
    print ("CNT Create Request")
    #print (payld)
    url = 'http://' + cseIP + ':' + csePort + '/' + parentID
    hdrs = {'X-M2M-RI':"CAE_Test",'X-M2M-Origin':originator, 'X-M2M-RVI':'2a' ,'Content-Type':"application/json;ty=3"}
    r = requests.post(url, data=dumps(payld), headers=hdrs)
    print ("CNT Create Response")
    print (r.text)

    return getResId('m2m:cnt',r)

def createSubscription(resourceName, parentID):
    payld = { "m2m:sub": { "rn": resourceName, "enc": {"net":[3]}, "nu":[originator],"acpi": ["cse-in/acpLightAppPolicy"]} }
    print ("Sub Create Request")
    #print (payld)
    url = 'http://' + cseIP + ':' + csePort + '/' + parentID
    hdrs = {'X-M2M-RI':"Sub",'X-M2M-Origin':originator, 'X-M2M-RVI':'2a' ,'Content-Type':"application/json;ty=23"}
    r = requests.post(url, data=dumps(payld), headers=hdrs)
    print ("SUB Create Response")
    print (r.text)

    return getResId('m2m:sub',r)


def createContentInstance(content, parentID):
    payld = { "m2m:cin": { "cnf": "application/text:0", "con": content} }
    print ("CI Create Request")
    #print (payld)
    url = 'http://' + cseIP + ':' + csePort + '/' + parentID
    hdrs = {'X-M2M-RI':"sensorValue",'X-M2M-Origin':originator, 'X-M2M-RVI':'2a' ,'Content-Type':"application/json;ty=4"}
    r = requests.post(url, data=dumps(payld), headers=hdrs)
    print ("CIN Create Response")
    print (r.text)

    return getResId('m2m:cin',r)


# The content of a <semanticdescriptor> shall be b64 encoded
def smdEncode(description):
    msgAscii = description.encode('ascii')  
    b64 = base64.b64encode(msgAscii)  
    descriptionb64 = b64.decode('ascii')  
    return descriptionb64

def buildEncodedSemanticDescriptor(prefix,triples):
    smdfull = prefix + triples
    #print(smdfull)

    g = Graph().parse(data=smdfull, format='n3')
    smdxml = g.serialize(format='xml', indent=4)
    #print(smdxml)
    smd2b64 = smdEncode(smdxml)
    return smd2b64

prefixes = '''@prefix saref: <https://saref.etsi.org/core/> .
@prefix s4envi: <https://saref.etsi.org/saref4envi/> .
@prefix s4city: <https://saref.etsi.org/saref4city/> .
@prefix geosp: <http://www.opengis.net/ont/geosparql#> .
@prefix sf: <http://www.opengis.net/ont/sf> .
@prefix dbr: <https://dbpedia.org/resource/> .
@prefix geo: <http://www.w3.org/2003/01/geo/wgs84_pos#> .
@prefix rev: <http://tutorial.etsi.org/vocabulary#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix : <http://tutorial.etsi.org/resources#> .  
@prefix m2m: <https://git.onem2m.org/MAS/BaseOntology/raw/master/base_ontology.owl#> .
  
'''


# smdPayload is read from file as passed as an arguement after b64 encoding
def createSMD(resourceName, parentID, reqId, smdPayload ):
    descriptor = smdPayload
    #print(descriptor)
    dsp = buildEncodedSemanticDescriptor(prefixes, descriptor)
    payld = { "m2m:smd": { "rn": resourceName, "dsp": dsp, "dcrp":4,"acpi": ["cse-in/acpLightAppPolicy"]} }

    print ("SMD Create Request")
    #print (payld)
    url = 'http://' + cseIP + ':' + csePort + '/' + parentID
    print(url)
    hdrs = {'X-M2M-RI':reqId,'X-M2M-Origin':originator, 'X-M2M-RVI':'2a' ,'Content-Type':"application/json;ty=24"}
    r = requests.post(url, data=dumps(payld), headers=hdrs)
    print ("SMD Create Response")
    print (r.text)

    return getResId('m2m:smd',r)

# From https://pysimplegui.readthedocs.io/en/latest/cookbook/#the-pysimplegui-cookbook
# The callback functions for the GUI elements
def button1():
    print('Send Illuminance callback')
    print(value["-Illuminance-"])
    # Create ContentInstance resource
    if cntIll:
        createContentInstance(value["-Illuminance-"], cntIll)


def button2():
    print('Send Luminescence callback')
    print(value["-Luminescence-"])
    # Create ContentInstance resource
    if cntLum:
        createContentInstance(value["-Luminescence-"], cntLum)

def button3():
    print('Send Phosphorescence callback')
    print(value["-Phosphorescence-"])
    # Create ContentInstance resource
    if cntPho:
        createContentInstance(value["-Phosphorescence-"], cntPho)

def button4():
    print('Send LightAbsorption callback')
    print(value["-LightAbsorption-"])
    # Create ContentInstance resource
    if cntLtA:
        createContentInstance(value["-LightAbsorption-"], cntLtA)

def button5():
    print('Send Lamp status callback')
    # Create ContentInstance resource
    # change the lamp state and update the button image
    global lamp1State
    if lamp1State == Lamp_OFF:
        window['5'].update(image_data=convert_to_bytes("streetLightOn.png", (40, 40)))
        lamp1State = Lamp_ON
    elif lamp1State == Lamp_ON:
        window['5'].update(image_data=convert_to_bytes("streetLightBlue.png", (40, 40)))
        lamp1State = Lamp_OFF
    if cntLtStatus:
         createContentInstance(lamp1State, cntLtStatus)

def lampCommandHandler():
    print('Send Lamp Command callback')
    print(value["-Lamp-"])
    # Create ContentInstance resource
    # change the lamp state and update the button image
    global lamp1State
    if value["-Lamp-"] == Lamp_ON:
        window['5'].update(image_data=convert_to_bytes("streetLightOn.png", (40, 40)))
        lamp1State = Lamp_ON
    elif value["-Lamp-"] == Lamp_OFF:
        window['5'].update(image_data=convert_to_bytes("streetLightBlue.png", (40, 40)))
        lamp1State = Lamp_OFF
    if cntLtStatus: # do not send the <cin> if we do not know the resourceID
          createContentInstance(lamp1State, cntLtStatus)

# Register Button callback is part of startup or reset process. When this application is started
# for the first time the basic resources are not present in the CSE. This callback will create
# all of the 'one-time' only resources, such as 'AE', 'container' and 'subscription' (and others as needed)
def buttonReg():
    print('Button Reg callback')
    # Create AE resource, then a container resource for each supported sensor
    aeRi = createAE(resourceName=deviceName)
    payload = smdAEPayld.replace("RESOURCE_ID", aeRi)
    createSMD(resourceName = "aeSMD", parentID = aeRi, reqId = "aeSMD",smdPayload = payload )
    if Illuminance == "YES":
        global cntIll
        cntIll = createContainer(resourceName = "Illuminance", parentID = aeRi)
        payload = smdSensorPayld.replace("RESOURCE_ID", cntIll)
        payload = payload.replace("PROPERTY","Illuminance")
        createSMD(resourceName = "sensorIllumSMD", parentID = cntIll, reqId = "sensorSMD",smdPayload = payload )

    if Luminescence == "YES":
        global cntLum
        cntLum = createContainer(resourceName = "Luminescence", parentID = aeRi)
        payload = smdSensorPayld.replace("RESOURCE_ID", cntLum)
        payload = payload.replace("PROPERTY","Luminescence")
        createSMD(resourceName = "sensorLumSMD", parentID = cntLum, reqId = "sensorSMD",smdPayload = payload )

    if Phosphorescence == "YES":
        global cntPho
        cntPho = createContainer(resourceName = "Phosphorescence", parentID = aeRi)
        payload = smdSensorPayld.replace("RESOURCE_ID", cntPho)
        payload = payload.replace("PROPERTY","Phosphorescence")
        createSMD(resourceName = "sensorPhosSMD", parentID = cntPho, reqId = "sensorSMD",smdPayload = payload )

    if LightAbsorption == "YES":
        global cntLtA
        cntLtA = createContainer(resourceName = "LightAbsorption", parentID = aeRi)
        payload = smdSensorPayld.replace("RESOURCE_ID", cntLtA)
        payload = payload.replace("PROPERTY","LightAbsorption")
        createSMD(resourceName = "sensorLghtAbsSMD", parentID = cntLtA, reqId = "sensorSMD",smdPayload = payload )

    if Lamp1 == "YES":

        cntLtStatus = createContainer(resourceName = "LightStatus", parentID = aeRi, mni = 1)
        payload = smdLightStatusPayld.replace("RESOURCE_ID", cntLtStatus)
        createSMD(resourceName = "ltCmdSMD", parentID = cntLtStatus, reqId = "ltCmdSMD",smdPayload = payload )
       
        global cntLtControl
        cntLtControl = createContainer(resourceName = "LightControl", parentID = aeRi, mni = 1)
        payload = smdLightCommandPayld.replace("RESOURCE_ID", cntLtControl)
        payload = payload.replace("ON_VALUE", Lamp_ON)
        payload = payload.replace("OFF_VALUE", Lamp_OFF)
        createSMD(resourceName = "ltCmdSMD", parentID = cntLtControl, reqId = "ltCmdSMD",smdPayload = payload )
        # create a subscription to the control container
        subLtControl = createSubscription(resourceName = "LightControlSub", parentID = cntLtControl)
    

def buttonDeReg():
    print('Button DeReg callback')
    deleteAE(resourceName=deviceName)

