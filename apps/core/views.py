from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.
def index(request):
    return render(request, 'index.html') 

def flight_search(request):
    return HttpResponse("Flight search page")

def login(request):
    return HttpResponse("Login Page")

def account_info(request): 
    return HttpResponse("Account Info")
