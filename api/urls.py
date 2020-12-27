from django.urls import path

from api import views
from api.views import Logout, Login, Record, Tickets, OrderTicket

urlpatterns = [
    path('addUser/', Record.as_view(), name="register"),
    path('login/', Login.as_view(), name="login"),
    path('logout/', Logout.as_view(), name="logout"),
    path('ticket/', Tickets.as_view(), name="logout"),
    path('order/', OrderTicket.as_view(), name="order"),
    path('snippets/<int:pk>', views.getUserTicket),

]
