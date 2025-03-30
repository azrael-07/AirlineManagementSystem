from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from apps.flights.models import Flight, Airport
from django.views.decorators.http import require_http_methods
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@require_http_methods(["GET", "POST"])
def flight_search(request):
    try:
        # Log the request method and data
        logger.info(f"Request method: {request.method}")
        logger.info(f"POST data: {request.POST}")
        logger.info(f"GET data: {request.GET}")

        # Determine if the request contains search parameters
        if request.method == "POST" or (request.method == "GET" and request.GET.get('departure')):
            # Use POST data if available, otherwise GET data
            data = request.POST if request.method == "POST" else request.GET

            # Log the data being used
            logger.info(f"Using data: {data}")

            # Look up the airports using the provided id
            departure = get_object_or_404(Airport, id=data.get('departure'))
            arrival = get_object_or_404(Airport, id=data.get('arrival'))
            departure_date = data.get('departure_date')
            
            if not departure_date:
                raise ValueError("Departure date is required")
                
            departure_date_obj = datetime.strptime(departure_date, "%Y-%m-%d").date()

            # Search for outbound flights
            outbound_flights = Flight.objects.filter(
                departure=departure,
                arrival=arrival,
                departure_time__date=departure_date_obj,
                status='Scheduled'
            )
            
            # Check for roundtrip
            return_date = data.get('return_date')
            return_flights = []
            if return_date:
                return_date_obj = datetime.strptime(return_date, "%Y-%m-%d").date()
                return_flights = Flight.objects.filter(
                    departure=arrival,
                    arrival=departure,
                    departure_time__date=return_date_obj,
                    status='Scheduled'
                )
            
            # Calculate minimum price and duration
            if outbound_flights:
                min_price = min(flight.price for flight in outbound_flights)
                min_duration = min(flight.duration for flight in outbound_flights)
            else:
                min_price = None
                min_duration = None

            context = {
                'outbound_flights': outbound_flights,
                'return_flights': return_flights,
                'airports': Airport.objects.all(),
                'min_price': min_price,
                'min_duration': min_duration,
                'form_data': {
                    'departure': departure.id,
                    'arrival': arrival.id,
                    'departure_date': departure_date,
                    'return_date': return_date,
                    'passengers': data.get('passengers'),
                    'payment_method': data.get('payment_method')
                }
            }
            
            # Log the context being passed to the template
            logger.info(f"Rendering flight_results.html with context: {context}")
            return render(request, 'flight_results.html', context)
        else:
            # No search parameters provided, show the search form
            return render(request, 'flight_search.html', {
                'airports': Airport.objects.all()
            })
    except Exception as e:
        logger.error(f"Error in flight_search view: {str(e)}")
        return render(request, 'flight_search.html', {
            'error': str(e),
            'airports': Airport.objects.all()
        })

def index(request):
    return render(request, 'index.html') 

def login(request):
    return render(request, 'login.html') 

def account_info(request): 
    return HttpResponse("Account Info")
