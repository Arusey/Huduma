from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User



def password_validator():
    return serializers.RegexField(
        regex=("^(?=.{8,}$)(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*"),
        max_length=128,
        min_length=8,
        write_only=True,
        required=True,
        error_messages={
            'required': 'please ensure you have inserted a password',
            'min_length': 'password cannot be less than 8 characters',
            'max-length': 'password cannot be greater than 50 characters',
            'invalid': 'please consider a password that has a number, an '
                       'uppercase letter, lowercase letter and'
                       ' a special character',
        }
    )


def email_validator():
    return serializers.EmailField(
        required=True,
        validators=[UniqueValidator(
                queryset=User.objects.all(),
                message='user with this email already exists.'
            )
            ],
        error_messages={
            'required': 'Ensure the email is inserted',
            'invalid': 'Enter a valid email address.'
        }
    )


class UserSerializer(serializers.ModelSerializer):

    date_joined = serializers.ReadOnlyField()


    password = password_validator()
    email = email_validator()


    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'date_joined', 'password')
        extra_kwargs = {'password': {'write_only': True}}
        