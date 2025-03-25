from django.http import HttpResponse
from django.shortcuts import render
from apps.flights.models import Flight, Airport
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from datetime import datetime
# Create your views here.
def index(request):
    return render(request, 'index.html') 

@require_http_methods(["GET", "POST"])
def flight_search(request):
    try:
        
        departure = get_object_or_404(Airport, code=request.POST.get('departure'))
        arrival = get_object_or_404(Airport, code=request.POST.get('arrival'))
        departure_date = request.POST.get('departure_date') 
        departure_date_obj = datetime.strptime(departure_date, "%Y-%m-%d").date()
        # Only calculate min values if flights exist
       
        flights = Flight.objects.filter(
            departure=departure.id,
            arrival=arrival.id,
            departure_time__date=departure_date_obj
        )
        if flights:
            min_price = min(flight.price for flight in flights)
            min_duration = min(flight.duration for flight in flights)
        else:
            min_price = None
            min_duration = None

        return render(request, 'flight_results.html', {
            'flights': flights,
            'airports' : Airport.objects.all(),
            'min_price': min_price,
            'min_duration': min_duration,
            'form_data':{
                'departure': departure,
                'arrival': arrival,
                'departure_date': departure_date,
                'passengers': request.POST.get('passengers'),
                'payment_method': request.POST.get('payment_method')
            }

            })
    except Exception as e:
        return render(request, 'flight_search.html' ,{
            'error':str(e)
        })



def login(request):
    return HttpResponse("Login Page")

def account_info(request): 
    return HttpResponse("Account Info")
