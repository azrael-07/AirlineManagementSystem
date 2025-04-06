from django.urls import path

from apps.checkin.views import checkin_baggage_view, checkin_payment_view, checkin_start_view, checkin_complete_view

urlpatterns = [
    
path("start/", checkin_start_view, name="checkin_start"),
path("baggage/", checkin_baggage_view, name="checkin_baggage"),
path("payment/", checkin_payment_view, name="checkin_payment"),
path("complete/", checkin_complete_view, name="checkin_complete"),
]