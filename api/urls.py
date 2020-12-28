from django.urls import path

from api import views
from api.views import Logout, Login, Record, Tickets, OrderTicket, GetTickets, AddTicket, CreateToken

urlpatterns = [
    path('register_user/', Record.as_view(), name="register"),
    path('login/', Login.as_view(), name="login"),
    path('logout/', Logout.as_view(), name="logout"),
    path('list_tickets/',GetTickets.as_view(), name="list_tickets"),
    path('add_ticket/', AddTicket.as_view(), name="add_ticket"),
    path('order_ticket/', OrderTicket.as_view(), name="order_ticket"),
    path('get_ticket/<int:pk>', views.getUserTicket),
    path('createUserToken', CreateToken.as_view()),

]
