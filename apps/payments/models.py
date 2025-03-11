from django.db import models

# Create your models here.
class PaymentStatus(models.TextChoices):
    APPROVED = 'approved','approved'
    PROCESSING = 'processing','processing'  
    INITIATED = 'initiated','initiated'
    FAILED = 'failed','failed'
    REFUNDED = 'refunded','refunded'

class Payment(models.Model):    
    payment_id = models.AutoField(primary_key=True)  
    amount = models.FloatField()
    status = models.CharField(max_length=255,choices=PaymentStatus.choices,default=PaymentStatus.INITIATED)
    reservation = models.OneToOneField('bookings.AirlineReservation', on_delete=models.CASCADE, related_name="payment")

    class Meta:
        abstract = True  # Makes Payment an abstract base class

    def __str__(self):
        return f"Payment {self.paymentID} - {self.status}"
   # Credit Card Payment
class CreditCard(Payment):
    name_on_card = models.CharField(max_length=100)
    last_four_digits = models.PositiveIntegerField()
    reservation = models.OneToOneField("bookings.AirlineReservation", on_delete=models.CASCADE, related_name="creditcard_payment")

    def __str__(self):
        return f"CreditCard Payment {self.payment_id} - {self.last_four_digits}"

# ACH Payment
class ACH(Payment):
    bank_name = models.CharField(max_length=100)
    acc_number_last_four = models.CharField(max_length=4)
    reservation = models.OneToOneField("bookings.AirlineReservation", on_delete=models.CASCADE, related_name="ach_payment")

    def __str__(self):
        return f"ACH Payment {self.paymentID} - {self.bank_name}"

# Cash Payment
class Cash(Payment):
    cash_tendered = models.DecimalField(max_digits=10, decimal_places=2)
    reservation = models.OneToOneField("bookings.AirlineReservation", on_delete=models.CASCADE, related_name="cash_payment")

    def __str__(self):
        return f"Cash Payment {self.paymentID} - Amount: {self.cash_tendered}"