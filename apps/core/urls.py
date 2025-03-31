from django.urls import path
from .views import flight_search, account_info, login,index, seat_selection,checkout_view

urlpatterns = [
    path('', index, name='index'),  # Add this line for index page
    path('flight-search/', flight_search, name='flight_search'),
    path('account_info/', account_info, name='account_info'),
    path('login/', login, name='login'),
    path('seat_selection/' ,seat_selection , name ='seat_selection' ) ,
    path('checkout/', checkout_view, name='checkout'),
]