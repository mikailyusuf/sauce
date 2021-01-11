import uuid

from django.db import models

from authentication.models import User


class Tickets(models.Model):
    start_destination = models.CharField(max_length=250, null=False)
    stop_destination = models.CharField(max_length=250, null=False)
    price = models.DecimalField(max_digits=50,decimal_places=2)
    ticket_id = models.CharField(max_length=500, null=True, default="")
    expired = models.BooleanField(default=False)
    used = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_created=True, auto_now=True)

    def __str__(self):
        return "{} -{}".format(self.start_destination, self.stop_destination)



class ReserverdTickets(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Tickets, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=255,default=uuid.uuid4,editable=False,unique = True)
    date_purchased = models.DateTimeField(auto_created=True, auto_now=True)

    def __str__(self):
        return str(self.order_id)
