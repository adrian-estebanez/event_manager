from rest_framework import serializers
from .models import Event, TicketType, Registration

class TicketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketType
        fields = ['id', 'name', 'price', 'available_quantity']

class EventSerializer(serializers.ModelSerializer):
    ticket_types = TicketTypeSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = [
            'id', 'name', 'description', 'location', 'start_date', 'end_date',
            'price', 'max_attendees', 'is_public', 'organizer', 'ticket_types'
        ]
        read_only_fields = ['organizer']

class EventCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'id', 'name', 'description', 'location', 'start_date', 'end_date',
            'price', 'max_attendees', 'is_public'
        ]

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = ['id', 'user', 'event', 'ticket_type', 'registered_at', 'qr_code']
        read_only_fields = ['user', 'registered_at', 'qr_code']
