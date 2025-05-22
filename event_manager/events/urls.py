from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import TicketTypeViewSet, RegistrationViewSet, EventStatsView, CancelRegistrationView, EventViewSet, EventInvitationViewSet


router = DefaultRouter()
router.register(r'', EventViewSet, basename='event')
router.register(r'tickets', TicketTypeViewSet, basename='ticket')
router.register(r'registrations',RegistrationViewSet, basename='registration')
router.register(r'invitaciones', EventInvitationViewSet, basename='invitacion')
urlpatterns = [
    path('', include(router.urls)),
    path('cancel-registration/<int:registration_id>/', CancelRegistrationView.as_view(), name='cancel-registration'),
    path('stats/<int:event_id>/', EventStatsView.as_view(), name='event-stats'),
    
    ]
