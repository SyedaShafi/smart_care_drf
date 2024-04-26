
from django.shortcuts import render, redirect
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from . models import Patient
from . serializers import PatientSerializer, RegistrationSerializer, UserLoginSerializer
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

# Create your views here.

class PatientViewset(viewsets.ModelViewSet):
    queryset = Patient.objects.all() #for PUT PATCH GET POST all the requests
    serializer_class = PatientSerializer


class UserRegistrationAPIView(APIView):
    serializer_class = RegistrationSerializer 
    def post(self, request):
        serializer = self.serializer_class(data = request.data)
       
        if serializer.is_valid():
            user = serializer.save()
            print(f"User: {user}")
            token = default_token_generator.make_token(user)
            print(f"token: {token}")
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            print(f"UID: {uid}")
            confirm_link = f"http://127.0.0.1:8000/patient/active/{uid}/{token}"
            email_subject = "Confirm Your Email"
            email_body = render_to_string('confirm_email.html', {'confirm_link' : confirm_link})

            email = EmailMultiAlternatives(email_subject, '', to=[user.email])

            email.attach_alternative(email_body, "text/html")

            email.send()
            return Response("Check your mail for confirmation")
        return Response(serializer.errors)
    

def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk = uid)
    except(User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    
    else:
        return redirect('register')
    


class UserLoginAPIView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data = self.request.data)
        if serializer.is_valid():
            username = serializer._validated_data['username']
            password = serializer._validated_data['password']

            user = authenticate(username = username, password = password)

            if user:
                token, create = Token.objects.get_or_create(user=user)
                login(request, user)
                return Response({'token': token.key, 'user_id': user.id})
            else:
                return Response({'error': "Invalid Credentials"})
        
        return Response(serializer.errors)



class UserLogoutView(APIView):
    def get(self, request):
        request.user.auth_token.delete()
        logout(request)
        return redirect('login')
        

