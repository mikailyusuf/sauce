from django.contrib import auth
from django.db import models


# Create your models here.
class User(auth.models.User):
    # username = models.CharField(max_length=255, null=False)
    # email = models.EmailField(max_length=255, null=False)
    is_admin = models.BooleanField(default=False)
    # password = models.CharField(max_length=50, null=False)
    ifLogged = models.BooleanField(default=False)
    token = models.CharField(max_length=500, null=True, default="")

    def __str__(self):
        return "{} -{}".format(self.id, self.email)


class Tickets(models.Model):
    start_destination = models.CharField(max_length=250, null=False)
    stop_destination = models.CharField(max_length=250, null=False)
    price = models.CharField(max_length=200, null=False)
    ticket_id = models.CharField(max_length=500, null=True, default="")
    expired = models.BooleanField(default=False)
    used = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_created=True, auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return "{} -{}".format(self.start_destination, self.stop_destination)


class UserTickets(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Tickets, on_delete=models.CASCADE)
    date_purchased = models.DateTimeField(auto_created=True, auto_now=True)

    def __str__(self):
        return str(self.date_purchased)


class ReserveTicket(models.Model):
    user_id = models.IntegerField()
    ticket_id = models.CharField(max_length=250)
