from uuid import uuid4

from django.db.models import Q
from requests import models
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from api.models import User, Tickets, UserTickets, ReserveTicket


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(max_length=8)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password'
        )


class UserLoginSerializer(serializers.ModelSerializer):
    # to accept either username or email
    user_id = serializers.CharField()
    password = serializers.CharField()
    token = serializers.CharField(required=False, read_only=True)

    def validate(self, data):
        # user,email,password validator
        user_id = data.get("user_id", None)
        password = data.get("password", None)
        if not user_id and not password:
            raise ValidationError("Details not entered.")
        user = None
        # if the email has been passed
        if '@' in user_id:
            user = User.objects.filter(
                Q(email=user_id) &
                Q(password=password)
            ).distinct()
            if not user.exists():
                raise ValidationError("User credentials are not correct.")
            user = User.objects.get(email=user_id)
        else:
            user = User.objects.filter(
                Q(username=user_id) &
                Q(password=password)
            ).distinct()
            if not user.exists():
                raise ValidationError("User credentials are not correct.")
            user = User.objects.get(username=user_id)
        if user.ifLogged:
            raise ValidationError("User already logged in.")
        user.ifLogged = True
        data['token'] = uuid4()
        user.token = data['token']
        user.save()
        return data

    class Meta:
        model = User
        fields = (
            'user_id',
            'password',
            'token',
        )

        read_only_fields = (
            'token',
        )


class UserLogoutSerializer(serializers.ModelSerializer):
    token = serializers.CharField()
    status = serializers.CharField(required=False, read_only=True)

    def validate(self, data):
        token = data.get("token", None)
        print(token)
        user = None
        try:
            user = User.objects.get(token=token)
            if not user.ifLogged:
                raise ValidationError("User is not logged in.")
        except Exception as e:
            raise ValidationError(str(e))
        user.ifLogged = False
        user.token = ""
        user.save()
        data['status'] = "User is logged out."
        return data

    class Meta:
        model = User
        fields = (
            'token',
            'status',
        )


class ReserveTicketSerializer(serializers.ModelSerializer):

    def validate(self, data):
        user_id = data.get("user_id", None)
        ticket_id = data.get("ticket_id", None)
        print(str(user_id) + str(ticket_id))
        try:
            user = User.objects.get(id=user_id)
            if not user:
                raise ValidationError("User Does not exist")
            try:
                print("Ticket ID " + ticket_id)
                ticket = Tickets.objects.get(ticket_id=ticket_id)
                userTicket = UserTickets.objects.create(user= user,ticket = ticket)
                try:
                    userTicket.save()
                except Exception as e:
                    print(str(e))
                if not ticket:
                    raise ValidationError("Ticket Does not exist")
            except Exception as e:
                raise ValidationError(str(e))

        except Exception as e:
            raise ValidationError(str(e))

        return  data

    class Meta:
        model = ReserveTicket
        fields = "__all__"



class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tickets
        fields = "__all__"


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tickets
        fields = "__all__"


class UserTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTickets
        fields = "__all__"
