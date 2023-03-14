"""Forms module for registration."""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from buyer.models import Genders


class RegisterForm(UserCreationForm):
    """Form for registration"""

    full_name = forms.CharField(max_length=100, label="Full name")
    age = forms.IntegerField()
    gender = forms.ChoiceField(
        choices=[(gender.name, gender.value) for gender in Genders]
    )

    class Meta:
        model = User
        fields = [
            "username",
            "password1",
            "password2",
            "email",
            "full_name",
            "age",
            "gender",
        ]
