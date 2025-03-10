from django.contrib import admin
from .models import CreditCard, ACH, Cash

@admin.register(CreditCard)
class CreditCardAdmin(admin.ModelAdmin):
    list_display = ("id", "name_on_card", "last_four_digits", "amount", "status", "reservation")
    search_fields = ("name_on_card", "last_four_digits", "reservation__reservationNumber")

@admin.register(ACH)
class ACHAdmin(admin.ModelAdmin):
    list_display = ("id", "bank_name", "acc_number_last_four", "amount", "status", "reservation")
    search_fields = ("bank_name", "acc_number_last_four", "reservation__reservationNumber")

@admin.register(Cash)
class CashAdmin(admin.ModelAdmin):
    list_display = ("id", "cash_tendered", "amount", "status", "reservation")
    search_fields = ("reservation__reservationNumber",)