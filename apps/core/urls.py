from django.urls import path
from .views import flight_search, account_info, login,index, seat_selection,checkout_view, confirmation_view, pilot_dashboard,crew_dashboard,frontdesk_dashboard

urlpatterns = [
    path('', index, name='index'),  # Add this line for index page
    path('flight-search/', flight_search, name='flight_search'),
    path('account_info/', account_info, name='account_info'),
    path('login/', login, name='login'),
    path('seat_selection/' ,seat_selection , name ='seat_selection' ) ,
    path('checkout/', checkout_view, name='checkout'),
    path('confirmation/', confirmation_view, name='confirmation'),
    path('error/', checkout_view, name='error'),
    path('pilot_dashboard/', pilot_dashboard, name='pilot_dashboard'),
    path('crew_dashboard/', crew_dashboard, name='crew_dashboard'),
    path('frontdesk_dashboard/', frontdesk_dashboard, name='frontdesk_dashboard'),

]