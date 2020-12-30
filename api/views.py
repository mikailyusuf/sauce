from django.shortcuts import redirect
# Create your views here.
from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from api.models import User, UserTickets, ReserveTicket, Tickets
from api.serializers import UserSerializer, UserLoginSerializer, UserLogoutSerializer, UserTicketSerializer, \
    ReserveTicketSerializer, TicketSerializer


@api_view(['GET', 'POST'])
def getUserTicket(request, pk):
    try:
        user = User.objects.get(id=pk)
        print(str(user))
        tickets = UserTickets.objects.filter(user=user)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        print("INSIDE GET")
        serializer = UserTicketSerializer(tickets, many=True)
        print(str(serializer.data))

        # if serializer.is_valid():
        #     print(str(serializer.data))
        return Response(serializer.data)
        return Response(serializer.errors)
    return Response(status=status.HTTP_400_BAD_REQUEST)


class CreateToken(APIView):

    def post(self, request):

        email = request.data["email"]
        password = request.data["password"]
        try:
            user = User.objects.get(email=email)
            print(str(user))
            token = Token.objects.create(user=user)
            print(token.key)
            data = {}
            data["token"] = str(token.key)
            return Response(status=status.HTTP_201_CREATED,data=data)


        except Exception as e:
            print(str(e))
            return Response(status=status.HTTP_400_BAD_REQUEST)


class AddTicket(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request, format=None):
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetTickets(APIView):

    def get(self, request, format=None):
        tickets = Tickets.objects.all()
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)


class OrderTicket(generics.CreateAPIView):
    queryset = ReserveTicket
    serializer_class = ReserveTicketSerializer


class Record(generics.CreateAPIView):
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
