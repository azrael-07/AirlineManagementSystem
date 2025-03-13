from django.urls import path
from .views import flight_search, account_info, login,index

urlpatterns = [
    path('', index, name='index'),  # Add this line for index page
    path('flight-search/', flight_search, name='flight_search'),
    path('account_info/', account_info, name='account_info'),
    path('login/', login, name='login'),
]