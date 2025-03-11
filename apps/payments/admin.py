from django.contrib import admin
from .models import CreditCard, ACH, Cash

@admin.register(CreditCard)
class CreditCardAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'amount', 'status', 'last_four_digits', 'reservation')
    list_filter = ('status',)
    actions = ['mark_as_successful']

    def mark_as_successful(self, request, queryset):
        for payment in queryset:
            payment.status = 'approved'
            payment.save()
            if payment.reservation:
                payment.reservation.update_reservation_number()

    mark_as_successful.short_description = "Mark selected CreditCard payments as Successful"

@admin.register(ACH)
class ACHAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'amount', 'status', 'bank_name', 'reservation')
    list_filter = ('status',)
    actions = ['mark_as_successful']

    def mark_as_successful(self, request, queryset):
        for payment in queryset:
            payment.status = 'approved'
            payment.save()
            if payment.reservation:
                payment.reservation.update_reservation_number()

    mark_as_successful.short_description = "Mark selected ACH payments as Successful"

@admin.register(Cash)
class CashAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'amount', 'status', 'cash_tendered', 'reservation')
    list_filter = ('status',)
    actions = ['mark_as_successful']

    def mark_as_successful(self, request, queryset):
        for payment in queryset:
            payment.status = 'approved'
            payment.save()
            if payment.reservation:
                payment.reservation.update_reservation_number()

    mark_as_successful.short_description = "Mark selected Cash payments as Successful"