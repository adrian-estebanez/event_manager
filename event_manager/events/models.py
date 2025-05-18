from django.db import models
from django.conf import settings
import qrcode
import io
import base64
from django.core.mail import send_mail
from django.template.loader import render_to_string 

class Event(models.Model):
    PUBLIC = 'public'
    PRIVATE = 'private'
    EVENT_TYPES = [
        (PUBLIC, 'Público'),
        (PRIVATE, 'Privado'),
    ]

    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='organized_events')
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    ticket_price = models.DecimalField(max_digits=8, decimal_places=2)
    max_attendees = models.PositiveIntegerField()
    event_type = models.CharField(max_length=10, choices=EVENT_TYPES, default=PUBLIC)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class TicketType(models.Model):
    event =models.ForeignKey(Event, on_delete=models.CASCADE, related_name='ticket_types')
    name = models.CharField(max_length=50)
    price= models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} - {self.event.name}"

class Registration(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='registrations')
    ticket_type = models.ForeignKey('TicketType', on_delete=models.CASCADE, related_name='registrations')
    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='registrations')
    registered_at = models.DateTimeField(auto_now_add=True)
    qr_code = models.TextField(blank=True)  

    def save(self, *args, **kwargs):
        is_new = self.pk is None  # Verifica si es una nueva inscripción (aún sin guardar)

        # Guardar primero para generar ID
        super().save(*args, **kwargs)

        # Generar QR si aún no existe
        if not self.qr_code:
            qr = qrcode.make(f'Registration ID: {self.id} - User: {self.user.email} - Event: {self.event.name}')
            buffer = io.BytesIO()
            qr.save(buffer, format="PNG")
            img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
            self.qr_code = img_str
            super().save(update_fields=['qr_code'])  # Guardar sólo el QR

        # Enviar correo de confirmación solo si es nuevo
        if is_new:
            subject = f"Confirmación de inscripción a {self.event.name}"
            message = render_to_string("emails/confirmacion.html", {
                'user': self.user,
                'event': self.event,
                'ticket': self.ticket_type,
                'qr': self.qr_code,
            })
            send_mail(subject, '', settings.DEFAULT_FROM_EMAIL, [self.user.email], html_message=message)

    def __str__(self):
        return f"{self.user.email} - {self.event.name} ({self.ticket_type.name})"


