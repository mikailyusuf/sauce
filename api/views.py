from django.shortcuts import render, redirect

# Create your views here.
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from api.models import User, UserTickets, ReserveTicket
from api.serializers import UserSerializer, UserLoginSerializer, UserLogoutSerializer, UserTicketSerializer, \
    ReserveTicketSerializer


@api_view(['GET', 'POST'])
def getUserTicket(request,pk):

    try:
        user = User.objects.get(id=pk)
        print(str(user))
        tickets = user.usertickets_set.all()
        print(str(tickets))
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        print("INSIDE GET")
        serializer = UserTicketSerializer(data=tickets)
        if(serializer.is_valid()):
            print(str(serializer.data))
            return Response(serializer.data)
    return  Response(status=status.HTTP_400_BAD_REQUEST)






class Tickets(generics.ListCreateAPIView):
    # get method handler
    queryset = UserTickets.objects.all()
    serializer_class = UserTicketSerializer


class OrderTicket(generics.CreateAPIView):

    queryset = ReserveTicket
    serializer_class = ReserveTicketSerializer

class Record(generics.ListCreateAPIView):
    # get method handler
    queryset = User.objects.all()
    serializer_class = UserSerializer


class Login(generics.GenericAPIView):
    # get method handler
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer_class = UserLoginSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            return Response(serializer_class.data, status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)


class Logout(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserLogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer_class = UserLogoutSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            return Response(serializer_class.data, status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)


def index(request):
    return redirect('/api/login')
