from django.shortcuts import render
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from datetime import datetime
import math
from .models import *
from .constant import FEE
# Create your views here.
@csrf_exempt
def flight(request):
    o_place = request.GET.get('Origin')
    d_place = request.GET.get('Destination')
    trip_type = request.GET.get('TripType')
    departdate = request.GET.get('DepartDate')
    depart_date = datetime.strptime(departdate, "%Y-%m-%d")
    return_date = None
    if trip_type == '2':
        returndate = request.GET.get('ReturnDate')
        return_date = datetime.strptime(returndate, "%Y-%m-%d")
        flightday2 = Week.objects.get(number=return_date.weekday()) ##
        origin2 = Place.objects.get(code=d_place.upper())   ##
        destination2 = Place.objects.get(code=o_place.upper())  ##
    seat = request.GET.get('SeatClass')

    flightday = Week.objects.get(number=depart_date.weekday())
    destination = Place.objects.get(code=d_place.upper())
    origin = Place.objects.get(code=o_place.upper())
    if seat == 'economy':
        flights = Flight.objects.filter(depart_day=flightday,origin=origin,destination=destination).exclude(economy_fare=0).order_by('economy_fare')
        try:
            max_price = flights.last().economy_fare
            min_price = flights.first().economy_fare    
        except:
            max_price = 0
            min_price = 0

        if trip_type == '2':    ##
            flights2 = Flight.objects.filter(depart_day=flightday2,origin=origin2,destination=destination2).exclude(economy_fare=0).order_by('economy_fare')    ##
            try:
                max_price2 = flights2.last().economy_fare   ##
                min_price2 = flights2.first().economy_fare  ##
            except:
                max_price2 = 0  ##
                min_price2 = 0  ##
                
    elif seat == 'business':
        flights = Flight.objects.filter(depart_day=flightday,origin=origin,destination=destination).exclude(business_fare=0).order_by('business_fare')
        try:
            max_price = flights.last().business_fare
            min_price = flights.first().business_fare
        except:
            max_price = 0
            min_price = 0

        if trip_type == '2':    ##
            flights2 = Flight.objects.filter(depart_day=flightday2,origin=origin2,destination=destination2).exclude(business_fare=0).order_by('business_fare')    ##
            try:
                max_price2 = flights2.last().business_fare   ##
                min_price2 = flights2.first().business_fare  ##
            except:
                max_price2 = 0  ##
                min_price2 = 0  ##

    elif seat == 'first':
        flights = Flight.objects.filter(depart_day=flightday,origin=origin,destination=destination).exclude(first_fare=0).order_by('first_fare')
        try:
            max_price = flights.last().first_fare
            min_price = flights.first().first_fare
        except:
            max_price = 0
            min_price = 0
            
        if trip_type == '2':    ##
            flights2 = Flight.objects.filter(depart_day=flightday2,origin=origin2,destination=destination2).exclude(first_fare=0).order_by('first_fare')
            try:
                max_price2 = flights2.last().first_fare   ##
                min_price2 = flights2.first().first_fare  ##
            except:
                max_price2 = 0  ##
                min_price2 = 0  ##    ##

    #print(calendar.day_name[depart_date.weekday()])
    if trip_type == '2':
        return render(request, "search.html", {
            'flights': flights,
            'origin': origin,
            'destination': destination,
            'flights2': flights2,   ##
            'origin2': origin2,    ##
            'destination2': destination2,    ##
            'seat': seat.capitalize(),
            'trip_type': trip_type,
            'depart_date': depart_date,
            'return_date': return_date,
            'max_price': math.ceil(max_price/100)*100,
            'min_price': math.floor(min_price/100)*100,
            'max_price2': math.ceil(max_price2/100)*100,    ##
            'min_price2': math.floor(min_price2/100)*100    ##
        })
    else:
        return render(request, "search.html", {
            'flights': flights,
            'origin': origin,
            'destination': destination,
            'seat': seat.capitalize(),
            'trip_type': trip_type,
            'depart_date': depart_date,
            'return_date': return_date,
            'max_price': math.ceil(max_price/100)*100,
            'min_price': math.floor(min_price/100)*100
        })

def review(request):
    flight_1 = request.GET.get('flight1Id')
    date1 = request.GET.get('flight1Date')
    seat = request.GET.get('seatClass')
    round_trip = False
    if request.GET.get('flight2Id'):
        round_trip = True

    if round_trip:
        flight_2 = request.GET.get('flight2Id')
        date2 = request.GET.get('flight2Date')

    if request.user.is_authenticated:
        flight1 = Flight.objects.get(id=flight_1)
        flight1ddate = datetime(int(date1.split('-')[2]),int(date1.split('-')[1]),int(date1.split('-')[0]),flight1.depart_time.hour,flight1.depart_time.minute)
        flight1adate = (flight1ddate + flight1.duration)
        flight2 = None
        flight2ddate = None
        flight2adate = None
        if round_trip:
            flight2 = Flight.objects.get(id=flight_2)
            flight2ddate = datetime(int(date2.split('-')[2]),int(date2.split('-')[1]),int(date2.split('-')[0]),flight2.depart_time.hour,flight2.depart_time.minute)
            flight2adate = (flight2ddate + flight2.duration)
        #print("//////////////////////////////////")
        #print(f"flight1ddate: {flight1adate-flight1ddate}")
        #print("//////////////////////////////////")
        if round_trip:
            return render(request, "book.html", {
                'flight1': flight1,
                'flight2': flight2,
                "flight1ddate": flight1ddate,
                "flight1adate": flight1adate,
                "flight2ddate": flight2ddate,
                "flight2adate": flight2adate,
                "seat": seat,
                "fee": FEE
            })
        return render(request, "book.html", {
            'flight1': flight1,
            "flight1ddate": flight1ddate,
            "flight1adate": flight1adate,
            "seat": seat,
            "fee": FEE
        })
    else:
        return HttpResponseRedirect(reverse("login"))



def book(request):
    if request.method == 'POST':
        flight_1 = request.POST.get('flight1')
        flight_1date = request.POST.get('flight1Date')
        flight_1class = request.POST.get('flight1Class')
        f2 = False
        if request.POST.get('flight2'):
            flight_2 = request.POST.get('flight2')
            flight_2date = request.POST.get('flight2Date')
            flight_2class = request.POST.get('flight2Class')
            f2 = True
        countrycode = request.POST['countryCode']
        mobile = request.POST['mobile']
        email = request.POST['email']
        flight1 = Flight.objects.get(id=flight_1)
        if f2:
            flight2 = Flight.objects.get(id=flight_2)
        passengerscount = request.POST['passengersCount']
        passengers = []
        for i in range(1, int(passengerscount) + 1):
            fname = request.POST[f'passenger{i}FName']
            lname = request.POST[f'passenger{i}LName']
            gender = request.POST[f'passenger{i}Gender']
            passengers.append(Passenger.objects.create(first_name=fname, last_name=lname, gender=gender.lower()))
        coupon = request.POST.get('coupon')

        try:
            ticket1 = createticket(None, passengers, passengerscount, flight1, flight_1date, flight_1class, coupon, countrycode, email, mobile)
            if f2:
                ticket2 = createticket(None, passengers, passengerscount, flight2, flight_2date, flight_2class, coupon, countrycode, email, mobile)

            if(flight_1class == 'Economy'):
                if f2:
                    fare = (flight1.economy_fare * int(passengerscount)) + (flight2.economy_fare * int(passengerscount))
                else:
                    fare = flight1.economy_fare * int(passengerscount)
            elif (flight_1class == 'Business'):
                if f2:
                    fare = (flight1.business_fare * int(passengerscount)) + (flight2.business_fare * int(passengerscount))
                else:
                    fare = flight1.business_fare * int(passengerscount)
            elif (flight_1class == 'First'):
                if f2:
                    fare = (flight1.first_fare * int(passengerscount)) + (flight2.first_fare * int(passengerscount))
                else:
                    fare = flight1.first_fare * int(passengerscount)
        except Exception as e:
            return HttpResponse(e)

        if f2:  ## 
            return render(request, "flight/payment.html", { ## 
                'fare': fare + FEE,  ## 
                'ticket': ticket1.id,  ## 
                'ticket2': ticket2.id  ## 
            })  ## 
        return render(request, "flight/payment.html", {
            'fare': fare + FEE,
            'ticket': ticket1.id
        })
    else:
        return HttpResponse("Method must be post.")
