from django.shortcuts import render

# Create your views here.
from rest_framework import permissions, status, generics
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from tickets.models import ReserverdTickets, Tickets
from tickets.serializers import TicketSerializer, ReservedTicketsSerializer, GetReservedTicketsSerializer


class AddTicket(generics.GenericAPIView):
    serializer_class = TicketSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        # request.user.is_staff
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        message = {"success": "Ticket Added  Successfully"}
        return Response(data=message, status=status.HTTP_201_CREATED)


class GetTickets(generics.GenericAPIView):
    serializer_class = TicketSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        tickets = Tickets.objects.all()
        serializer = self.serializer_class(tickets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class ReservedTicketsView(generics.GenericAPIView):
    serializer_class = ReservedTicketsSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response({"Success":"Ticket Reserved"})
            # serializer.save(owner=self.request.user)

    def get(self,request):
        user = request.user
        reserved_tickets = ReserverdTickets.objects.filter(user = user)
        serializer = GetReservedTicketsSerializer(reserved_tickets,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
