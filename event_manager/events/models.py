from django.db import models
from django.conf import settings

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
