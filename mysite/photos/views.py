from django.shortcuts import render
from .forms import PhotoUpload
import numpy as np
import os.path
import binascii
import face_recognition
import requests
from json import dumps
import time
import math
from django.contrib import messages

def photo_upload_view(request):
    
    if request.method == "POST":
        form = PhotoUpload(request.POST, request.FILES)
        if form.is_valid():

            # saves the image into the media folder and gets it bc its latest image
            form.save()
            folder_path ="./media/images"
            recent = 0
            recent_file = None
            for entry in os.scandir(folder_path):
                if entry.is_file():
                    mod_time = entry.stat().st_mtime_ns
                    if mod_time > recent:
                        recent_file = entry.name
                        recent = mod_time

            print("hi")
            
            # getting the hex and putting it into a content instance
            try:
                file_path = folder_path +"/" + str(recent_file)
                new_hex = str(encode(file_path))
                if new_hex == "ERROR":
                    raise Exception("Bad Hex")
                part_length = 750
                num_parts = math.ceil(len(new_hex) / part_length) 
                print("Total length: " + str(len(new_hex)) + "\nPart length: " + str(part_length) + "\nNum of parts: " + str(num_parts ))
                print("hi2")
                parts = [new_hex[i:i+part_length] for i in range(0, len(new_hex), part_length)]
                print("split success")
                print(len(parts))
                messages.success(request, "You successfully uploaded an Image!")


                # creation of the content instance for the hex

                
                print ("CI Create Request")
                url = 'http://35.89.20.163:8080/psu23-cse/lamppost-F1/thingy91'
                hdrs = {'X-M2M-RI':"sensorValue",'X-M2M-Origin':"CF1", 'X-M2M-RVI':'2a' ,'Content-Type':"application/json;ty=4"}
                # payld = { "m2m:cin": { "cnf": "application/text:0", "con": new_hex} }
                # r = requests.post(url, data=dumps(payld), headers=hdrs)

                #message = []
                count = 1
                for part in parts:
                    payld = { "m2m:cin": { "cnf": "application/text:0", "con": part} }
                    r = requests.post(url, data=dumps(payld), headers=hdrs)
                    time.sleep(5)
                    print(part[:5])
                    #message.append("part " + str(count) + " of "+ str(num_parts) +" is uploaded")
                num = 1



                return render(request, "home.html", {"num": num})
            
            except:
                messages.error(request, "There is problem is file upload!")
                num = 0
                #message = "Photo NOT UPLOADED.........."
                return render(request, "upload.html", {"num": num})
    
    else:
        form = PhotoUpload()
    return render(request, "upload.html", {"form": form})

# function to encode the image into hex
def encode(f):

    try:
        ab_image = face_recognition.load_image_file(f)
        ab_encoding = face_recognition.face_encodings(ab_image)[0]
        print(os.getcwd())
        np.savetxt("abencoding.txt",ab_encoding)
        with open('abencoding.txt', 'rb') as fp:
            hexstring = binascii.hexlify(fp.read())

        print("Encoded Successfully!!")

        print(len(hexstring))      

        return hexstring
    except:
        return "ERROR"

    
