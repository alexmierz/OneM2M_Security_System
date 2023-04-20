from django.shortcuts import render
from .forms import PhotoUpload
import numpy as np
import os.path
import binascii
import face_recognition
import face_recognition as faceRegLib
import dlib

def photo_upload_view(request):
    
    if request.method == "POST":
        form = PhotoUpload(request.POST, request.FILES)
        if form.is_valid():
            # handle_uploaded_file(request.FILES.get("file"))
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
            print(recent_file)
            file_path = folder_path +"/" + str(recent_file)
            encode(file_path)
           
            return render(request, "home.html")
        print("success!")
    else:
        form = PhotoUpload()
    return render(request, "upload.html", {"form": form})

def encode(f):
    ab_image = face_recognition.load_image_file(f)
    ab_encoding = face_recognition.face_encodings(ab_image)[0]
    np.savetxt("abencoidng.txt",ab_encoding)
    with open('abencoding.txt', 'rb') as fp:
        hexstring = binascii.hexlify(fp.read())

    print(hexstring)

    with open('ab.text','wb') as fp:
        b = np.loadtxt("ab.txt")
    print(b)
