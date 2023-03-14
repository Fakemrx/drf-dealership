"""Registration-attached views module."""
from django.shortcuts import render

from buyer.views.registration_form import RegisterForm


def register(response):
    """Registration logic."""
    form = RegisterForm(response.POST or None)
    if response.method == "POST":
        if form.is_valid():
            user = form.save()
            user.buyer.full_name = form.cleaned_data.get("full_name")
            user.buyer.age = form.cleaned_data.get("age")
            user.buyer.gender = form.cleaned_data.get("gender")
            user.buyer.balance = 0.00
            user.buyer.is_active = True
            user.save()
            return render(response, "registration done.html")
        render(response, "register.html", {"form": form, "errors": form.errors})

    return render(response, "register.html", {"form": form})
