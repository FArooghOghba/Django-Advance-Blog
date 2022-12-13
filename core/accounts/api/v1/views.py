from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken as BaseObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT, HTTP_200_OK

from rest_framework_simplejwt.views import TokenObtainPairView
from mail_templated import EmailMessage

from .serializers import (
    RegistrationModelSerializer, CustomAuthTokenSerializer,
    CustomTokenObtainSerializer, ChangePasswordModelSerializer,
    ProfileModelSerializer
)

from ...models import Profile
from ..utils import EmailThread


User = get_user_model()


class RegistrationGenericAPIView(GenericAPIView):
    serializer_class = RegistrationModelSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            data = {
                'email': serializer.validated_data['email']
            }
            return Response(data, status=HTTP_201_CREATED)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class ObtainAuthToken(BaseObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


class DiscardAuthToken(APIView):
    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainSerializer


class ChangePasswordUpdateAPIView(GenericAPIView):
    model = User
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordModelSerializer

    def get_object(self):
        user_obj = self.request.user
        return user_obj

    def put(self, request, *args, **kwargs):
        user_obj = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']

            if not user_obj.check_password(old_password):
                return Response(
                    {'wrong password': 'Old password is not correct'},
                    status=HTTP_400_BAD_REQUEST
                )

            user_obj.set_password(new_password)
            user_obj.save()
            return Response(
                {'new_password': 'Password changed successfully.'},
                status=HTTP_200_OK
            )

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class ProfileRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileModelSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        queryset = self.get_queryset()
        user = self.request.user
        profile = get_object_or_404(queryset, user=user)
        return profile


class ActivationConfirmGenericAPIView(GenericAPIView):
    def get(self, request, *args, **kwargs):
        activation_email = EmailMessage(
            'email/email.tpl',
            {'username': 'user_name'},
            'from_email@example.com',
            ['user.email@example.com']
        )
        EmailThread(activation_email).start()

        return Response('Emil Sent.')

"""
from django.core.mail import send_mail, EmailMessage
from django.template.loader import get_template

data = {
            "fname": 'username',
            "date": 'date',
        }

        message = get_template('email.html').render(data)
        email = EmailMessage(
            "About your appointment",
            message,
            'from@example.com',
            ['to@example.com'],
        )
        email.content_subtype = "html"
        email.send()
"""

"""
from mail_templated import send_mail

send_mail(
    'email/email.tpl',
    {'username': 'user_name'},
    'from_email@example.com',
    ['user.email@example.com']
)
"""