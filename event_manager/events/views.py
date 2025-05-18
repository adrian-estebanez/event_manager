from django.shortcuts import render
from event_manager import settings
from rest_framework import viewsets, permissions
from .models import Event
from .serializers import EventSerializer
from .models import TicketType, Registration
from .serializers import TicketTypeSerializer, RegistrationSerializer
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from rest.framework.permissions import IsAuthenticated


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
    permission_classes = [permissions.IsAutenticated]

class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = TicketType.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.IsAutenticated]

    def perform_create (self, serializer):
        ticket_type = serializer.validated_data['ticket_type']
        serializer.save(
            user=self.request.user,
            event=ticket_type.event
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
            message=f"Tu inscripción al evento '{event_name}' ha sido cancelada.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[request.user.email],
        )

        return Response({"message": "Inscripción cancelada exitosamente."}, status=status.HTTP_200_OK)

