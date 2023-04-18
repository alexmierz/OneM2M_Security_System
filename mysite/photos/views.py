from django.shortcuts import render
from .forms import PhotoUpload

import binascii

def photo_upload_view(request):
    if request.method == "POST":
        form = PhotoUpload(request.POST, request.FILES)
        if form.is_valid():
            # handle_uploaded_file(request.FILES.get("file"))
            form.save()
            return render(request, "home.html")
    else:
        form = PhotoUpload()
    return render(request, "upload.html", {"form": form})

def handle_uploaded_file(f):
    with open("some/file/name.txt", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def convert_to_hex(image):
    with image.open('rb') as f:
        hex_data = binascii.hexlify(f.read())
    return hex_data.decode('utf-8')

