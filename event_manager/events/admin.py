from django.contrib import admin
from .models import Event, TicketType, Registration

# Register your models here.

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'start_time', 'end_time')
    search_fields = ('name', 'location')
    list_filter = ('start_time',)
    ordering = ('start_time',)

@admin.register(TicketType)
class TicketTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'event')
    list_filter = ('event',)
    search_fields = ('name',)

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'ticket_type', 'registered_at')
    list_filter = ('event', 'ticket_type')
    search_fields = ('user__email', 'event__name')
    ordering = ('-registered_at',)