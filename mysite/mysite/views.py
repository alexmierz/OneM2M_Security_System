from django.shortcuts import render

def status(request):
    return render(request, 'templates/status.html')