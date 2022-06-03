# from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from . import forms
UserModel = get_user_model()

# Create your views here.


def signup(request):

    if request.method == "GET":
        # creates the userform and
        # renders the signup page with the createuser form

        form = forms.CreateUserForm()
        return render(request, "accounts/signup.html", {"form": form})
    if request.method == "POST":
        # if the form is valid then create the user and send an email to ask
        # the user to confirm and activate their account
        # if the form is not valid then render the signup page with the form

        form = forms.CreateUserForm(request.POST)
        if form.is_valid():
            print("is valid")
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = "Activate your account"
            message = render_to_string('accounts/account_active_email.html', {
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get("email")
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return render(request, "accounts/confirm_email_request.html")
        else:
            print("is not valid")
            form = forms.CreateUserForm()
            return render(request, "accounts/signup.html", {"form": form})


def activate(request, uidb64, token):
    # activate the account if the user confirms their account via email
    # if the link is invalid display message that the link is invalid
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect("accounts:login")
        # return HttpResponse("Thank you for confirmation. Now you can login")
    else:
        return render(request, "accounts/activation_link_invalid.html")
