from rest_framework import serializers
from rest_framework.status import HTTP_400_BAD_REQUEST

from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from ...models import User


class RegistrationModelSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=255, write_only=True,
        style={'input_type': 'password'}
    )

    confirm_password = serializers.CharField(
        max_length=255, write_only=True,
        style={'input_type': 'password'}
    )
    class Meta:
        model = User
        fields = ('email', 'password', 'confirm_password')

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        if not password == confirm_password:
            raise serializers.ValidationError(
                _('Password doesnt match.'),
                code=HTTP_400_BAD_REQUEST
            )

        try:
            validate_password(password)
        except ValidationError as error:
            raise serializers.ValidationError({'password': list(error.messages)})

        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        return self.objects.create_user(**validated_data)


class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label=_("Email"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            # The "authenticate" call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
