from django.shortcuts import render

def homepage(request):
    return render(request, "home.html")

def portalpage(request):
    return render(request, "portal.html")

def createquizzpage(request):
    return render(request, "createquiz.html")
