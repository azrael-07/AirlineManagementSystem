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
    if request.method == "GET":
        airports = Airport.objects.all()
        return render(request, 'flight_search.html',{
            'airports' : airports
        })
    departure = get_object_or_404(Airport, code=request.POST.get('departure'))
    arrival = get_object_or_404(Airport, code=request.POST.get('arrival'))
    departure_date = request.POST.get('departure_date') 
    departure_date_obj = datetime.strptime(departure_date, "%Y-%m-%d").date()
    flights = Flight.objects.filter(
        departure=departure.id,
        arrival=arrival.id,
        departure_time__date=departure_date_obj
    )

    return render(request, 'flight_results.html', {'flights': flights})

def login(request):
    return HttpResponse("Login Page")

def account_info(request): 
    return HttpResponse("Account Info")
