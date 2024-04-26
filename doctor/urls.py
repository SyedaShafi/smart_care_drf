from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

# Create a router and register our ViewSets with it.
router = DefaultRouter()
router.register('list', views.DoctorViewset)
router.register('review', views.ReviewViewset)
router.register('designation', views.DesignationViewset)
router.register('specialization', views.SpecializationViewset)
router.register('available_time', views.AvailableTimeViewset)


# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]