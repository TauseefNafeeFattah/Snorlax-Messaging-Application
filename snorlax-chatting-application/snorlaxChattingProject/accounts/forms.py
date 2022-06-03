from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class CreateUserForm(UserCreationForm):
    # The user form to create a user in Django backend
    class Meta:
        fields = ("username", "email")
        model = get_user_model()
