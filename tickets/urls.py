from django.urls import path

from tickets.views import ReservedTicketsView, AddTicket, GetTickets

urlpatterns = [
    # path('reserve_tickets', ReservedTicketsView.as_view(), name="reserver_Tickets"),
    path('add_ticket', AddTicket.as_view(), name="add-ticket"),
    path('get_tickets', GetTickets.as_view(), name="add-ticket"),
    path('reserve_ticket', ReservedTicketsView.as_view(), name="add-ticket"),


]