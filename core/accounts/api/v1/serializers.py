from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.status import HTTP_400_BAD_REQUEST

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from ...models import Profile

User = get_user_model()


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

            if not user.is_verified:
                raise serializers.ValidationError(
                    {'verification': "user is not verified."},
                    code=HTTP_400_BAD_REQUEST
                )
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class CustomTokenObtainSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        validated_data = super().validate(attrs)

        if not self.user.is_verified:
            raise serializers.ValidationError(
                {'verification': "user is not verified."},
                code=HTTP_400_BAD_REQUEST
            )

        validated_data['user_email'] = self.user.email
        validated_data['user_id'] = self.user.id

        return validated_data


class ChangePasswordModelSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        max_length=255, write_only=True, required=True,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        max_length=255, write_only=True, required=True, validators=[validate_password],
        style={'input_type': 'password'}
    )
    confirm_new_password = serializers.CharField(
        max_length=255, write_only=True, required=True,
        style={'input_type': 'password'}
    )

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        confirm_new_password = attrs.get('confirm_new_password')

        if not new_password == confirm_new_password:
            raise serializers.ValidationError(
                {'password': "Password fields didn't match"},
                code=HTTP_400_BAD_REQUEST
            )

        try:
            validate_password(attrs.get('new_password'))
        except ValidationError as e:
            raise serializers.ValidationError(
                {'new_password': list(e.messages)}
            )

        return super().validate(attrs)


class ProfileModelSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    class Meta:
        model = Profile
        fields = (
            'id', 'email', 'first_name', 'last_name', 'image', 'description'
        )


"""
class ChangePasswordModelSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(
        max_length=255, write_only=True, required=True,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        max_length=255, write_only=True, required=True, validators=[validate_password],
        style={'input_type': 'password'}
    )
    confirm_new_password = serializers.CharField(
        max_length=255, write_only=True, required=True,
        style={'input_type': 'password'}
    )
    class Meta:
        model = User
        fields = ('old_password', 'new_password', 'confirm_new_password')

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        confirm_new_password = attrs.get('confirm_new_password')

        if not new_password == confirm_new_password:
            raise serializers.ValidationError(
                {'password': "Password fields didn't match"},
                code=HTTP_400_BAD_REQUEST
            )
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user

        if not user.check_password(value):
            raise serializers.ValidationError(
                {'wrong password': 'Old password is not correct'}
            )
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()

        return instance

"""
