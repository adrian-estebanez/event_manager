from urllib import request
from django.shortcuts import render
from event_manager import settings
from rest_framework import viewsets, permissions, status
from .serializers import EventInvitationSerializer, EventSerializer
from .models import TicketType, Registration, Event, EventIvitation
from .serializers import TicketTypeSerializer, RegistrationSerializer
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated
from django.conf import settings

from events import serializers

class IsOrganizerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or obj.organizer == request.user

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated, IsOrganizerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

class TicketTypeViewSet(viewsets.ModelViewSet):
    queryset = TicketType.objects.all()
    serializer_class = TicketTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = TicketType.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        event = serializer.validated_data['event']
        user = self.request.user

        if event.es_privado:
            if not EventIvitation.objects.filter(event=event, user=user).exists():
                raise serializers.ValidationError("No estás invitado a este evento.")
            
        registration = serializer.save(user=self.request.user)

        send_mail(
            subject='Inscripción confirmada',
            message=f'Te has inscrito correctamente al evento "{event.name}".',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[request.user.email],
        )

    

class CancelRegistrationView(APIView):
    permission_classes = [IsAuthenticated] 

    def delete(self, request, registration_id):
        try:
            registration = Registration.objects.get(id=registration_id, user=request.user)
        except Registration.DoesNotExist:
            return Response({"error": "Inscripción no encontrada."}, status=status.HTTP_404_NOT_FOUND)

        # Guardamos los datos antes de eliminar
        event_name = registration.event.name

        # Eliminar inscripción
        registration.delete()

        # Enviar correo de cancelación
        send_mail(
            subject="Cancelación de inscripción",
            message=f"Tu inscripción al evento '{registration.event.name}' ha sido cancelada.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[request.user.email],
        )

        return Response({"message": "Inscripción cancelada exitosamente."}, status=status.HTTP_200_OK)
    

class EventStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, event_id):
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({"error": "Evento no encontrado."}, status=404)

        registrations = Registration.objects.filter(event=event)
        total_registrations = registrations.count()
        total_revenue = sum([r.ticket_type.price for r in registrations])

        ticket_summary = {}
        for ticket_type in event.ticket_types.all():
            count = registrations.filter(ticket_type=ticket_type).count()
            ticket_summary[ticket_type.name] = {
                "sold": count,
                "total": float(ticket_type.price * count)
            }

        return Response({
            "event": event.name,
            "registrations": total_registrations,
            "revenue": float(total_revenue),
            "tickets": ticket_summary
        })

class EventInvitationViewSet(viewsets.ModelViewSet):
    serializer_class = EventInvitationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return EventIvitation.objects.filter(event__organizer=self.request.user)

    def perform_create(self, serializer):
        invitation = serializer.save()
        invitation.enviado = True
        invitation.save()

       
        send_mail(
            subject="Estás invitado a un evento privado",
            message=f"Has sido invitado al evento: {invitation.event.name}.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[invitation.user.email],
        )
