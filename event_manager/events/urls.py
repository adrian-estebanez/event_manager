from rest_framework.routers import DefaultRouter
from .views import CancelRegistrationView, EventViewSet
from django.urls import path, include
from .views import TicketTypeViewSet, RegistrationViewSet


router = DefaultRouter()
router.register(r'', EventViewSet, basename='event')
router.register(r'tickets', TicketTypeViewSet, basename='ticket')
router.register(r'registrations',RegistrationViewSet, basename='registration')
urlpatterns = [
    path('', include(router.urls)),
    path('cancel-registration/<int:registration_id>/', CancelRegistrationView.as_view(), name='cancel-registration'),
]
