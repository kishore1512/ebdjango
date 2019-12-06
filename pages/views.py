from django.shortcuts import render
from django.http import HttpResponse


def homePageView(request):
    return HttpResponse('<center><h2>Hello All,</h2><br><h2> Welcome to Ibexlabs DevOps team. Cheers!!! Testing deployement</h2></center>')
# Create your views here.
