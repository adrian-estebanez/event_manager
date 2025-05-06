from rest_framework.routers import DefaultRouter
from .views import EventViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'', EventViewSet, basename='event')

urlpatterns = [
    path('', include(router.urls)),
]
