# Create your views here.
from pickle import TRUE
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth import authenticate, login
from django.forms.utils import ErrorList
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from .forms import LoginForm, SignUpForm
from django.template import loader
from django import template
from core.settings import AUTH_USER_MODEL as User


def redirect_login_view(request):
    return redirect('auth:login')


def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            # check the credential
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("/master/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):

    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            msg = 'New user registered successfully !!'
            success = True
            # redirect to login view if user is registered
            return render(request, "accounts/register.html", {"form": SignUpForm(), "msg": msg,"status":success})

        else:
            msg = form.errors
            print(msg)
            return render(request, "accounts/register.html", {"form": SignUpForm(), "msg": msg,"status":success})
    else:
        form = SignUpForm()

        return render(request, "accounts/register.html", {"form": SignUpForm(), "msg": msg,"status":success})
