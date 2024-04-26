from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . views import PatientViewset, UserRegistrationAPIView, activate, UserLoginAPIView, UserLogoutView

# Create a router and register our ViewSets with it.
router = DefaultRouter()
router.register('list', PatientViewset)


# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegistrationAPIView.as_view(), name='register'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('active/<uid64>/<token>', activate, name='activate')
]