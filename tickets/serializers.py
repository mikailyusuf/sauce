from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from tickets.models import ReserverdTickets, Tickets




class GetReservedTicketsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReserverdTickets
        fields = ("ticket", "date_purchased", "order_id")
        depth = 1


class ReservedTicketsSerializer(serializers.ModelSerializer):
    ticket_id = serializers.IntegerField()
    class Meta:
        model = ReserverdTickets
        fields = ['ticket_id']

    def validate(self, attrs):
        ticket_id = attrs.get('ticket_id', '')

        user = self.context['request'].user
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')

        try:
            ticket = Tickets.objects.get(id=ticket_id)
        except Tickets.DoesNotExist:
            raise AuthenticationFailed('Ticket Does not Exist,Please Provide a valid Ticket')

        reserved = ReserverdTickets.objects.create(user=user,ticket=ticket)
        print(reserved)

        return super().validate(attrs)




class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tickets
        fields = "__all__"
