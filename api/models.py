from django.db import models


# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100, blank=True, default='')
    email = models.CharField(max_length=100, blank=True, default='')
    phone = models.CharField(max_length=100, blank=True, default='')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} -{}".format(self.name, self.email)
