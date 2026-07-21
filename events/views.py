from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages


def home(request):
    return render(request, 'home.html')


def login_view(request):
    return render(request, 'login.html')


def register_view(request):

    if request.method == "POST":

        full_name = request.POST["full_name"]
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        # Check passwords
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        # Check username
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")

        # Check email
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("register")

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        # Save full name
        user.first_name = full_name
        user.save()

        messages.success(request, "Account created successfully.")
        return redirect("login")

    return render(request, "register.html")