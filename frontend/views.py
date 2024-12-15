from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
import math
from .models import *
# Create your views here.
def index(request):
    return render(request,'index.html')

def flight_search(request):
    return render(request,'search.html')

def contact(request):
    return render(request, 'contact.html')

def privacy_policy(request):
    return render(request, 'privacy-policy.html')

def terms_and_conditions(request):
    return render(request, 'terms.html')

def about_us(request):
    return render(request, 'about.html')

