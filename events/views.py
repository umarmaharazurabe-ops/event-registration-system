import qrcode
import tempfile
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q
from .models import Event, Registration
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages


def home(request):
    context = {
        "total_events": Event.objects.count(),
        "total_users": User.objects.count(),
        "total_registrations": Registration.objects.count(),
    }
    return render(request, "home.html", context)


def login_view(request):

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("dashboard")

        else:

            messages.error(request, "Invalid username or password.")

    return render(request, "login.html")

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
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

@login_required
def dashboard(request):

    total_events = Event.objects.count()
    total_registrations = Registration.objects.count()
    total_users = User.objects.count()
    recent_events = Event.objects.all().order_by("-id")[:5]

    context = {
        "total_events": total_events,
        "total_registrations": total_registrations,
        "total_users": total_users,
        "recent_events": recent_events,
    }

    return render(
        request,
        "dashboard.html",
        context
    )
def event_list(request):

    query = request.GET.get("q")
    category = request.GET.get("category")


    events = Event.objects.all()


    if query:
        events = events.filter(
            Q(title__icontains=query) |
            Q(category__icontains=query) |
            Q(location__icontains=query)
        )


    if category:
        events = events.filter(
            category=category
        )


    context = {
        "events": events
    }


    return render(
        request,
        "events.html",
        context
    )
def event_detail(request, id):

    event = get_object_or_404(Event, id=id)

    context = {
        "event": event
    }

    return render(request, "event_detail.html", context)
@login_required
def register_event(request, id):

    event = get_object_or_404(Event, id=id)


    current_registrations = Registration.objects.filter(
        event=event
    ).count()


    if current_registrations >= event.seats:

        messages.error(
            request,
            "Sorry, this event is already full."
        )

        return redirect(
            "event_detail",
            id=id
        )


    registration, created = Registration.objects.get_or_create(
        user=request.user,
        event=event
    )


    if created:

        messages.success(
            request,
            "You have registered successfully."
        )

    else:

        messages.info(
            request,
            "You already registered for this event."
        )


    return redirect(
        "event_detail",
        id=id
    )
@login_required
def my_registrations(request):

    registrations = Registration.objects.filter(
        user=request.user
    )

    context = {
        "registrations": registrations
    }

    return render(
        request,
        "my_registrations.html",
        context
    )
def logout_view(request):

    logout(request)

    return redirect("home")
@login_required
def profile(request):

    return render(
        request,
        "profile.html"
    )
@login_required
def register_event(request, id):

    event = get_object_or_404(Event, id=id)

    registration, created = Registration.objects.get_or_create(
        user=request.user,
        event=event
    )

    if created:
        messages.success(
            request,
            "You have successfully registered for this event."
        )
    else:
        messages.info(
            request,
            "You are already registered for this event."
        )

    return redirect("my_registrations")
@login_required
def my_registrations(request):

    registrations = Registration.objects.filter(
        user=request.user
    )

    context = {
        "registrations": registrations
    }

    return render(
        request,
        "my_registrations.html",
        context
    )
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def edit_profile(request):

    if request.method == "POST":

        request.user.first_name = request.POST.get("full_name")
        request.user.email = request.POST.get("email")

        request.user.save()

        messages.success(
            request,
            "Profile updated successfully."
        )

        return redirect("profile")

    return render(
        request,
        "edit_profile.html"
    )
@login_required
def change_password(request):

    if request.method == "POST":

        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():

            user = form.save()

            update_session_auth_hash(request, user)

            messages.success(
                request,
                "Password changed successfully."
            )

            return redirect("profile")

    else:

        form = PasswordChangeForm(request.user)

    return render(
        request,
        "change_password.html",
        {
            "form": form
        }
    )
@login_required
def download_ticket(request, id):

    registration = get_object_or_404(
        Registration,
        id=id,
        user=request.user
    )

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="ticket_{registration.id}.pdf"'
    )

    pdf = canvas.Canvas(response)

    pdf.setTitle("Event Ticket")

    pdf.setFont("Helvetica-Bold", 22)
    pdf.drawString(170, 800, "EVENT TICKET")

    pdf.setFont("Helvetica", 14)
    pdf.drawString(60, 740, f"Name: {registration.user.first_name}")
    pdf.drawString(60, 710, f"Event: {registration.event.title}")
    pdf.drawString(60, 680, f"Category: {registration.event.category}")
    pdf.drawString(60, 650, f"Location: {registration.event.location}")
    pdf.drawString(60, 620, f"Date: {registration.event.event_date}")
    pdf.drawString(60, 590, f"Time: {registration.event.event_time}")
    pdf.drawString(60, 560, f"Registration ID: {registration.id}")

    pdf.line(50, 540, 550, 540)
    pdf.drawString(60, 510, "Thank you for registering.")

    # QR Code
    qr_data = f"""
Registration ID: {registration.id}
Name: {registration.user.first_name}
Event: {registration.event.title}
Location: {registration.event.location}
Date: {registration.event.event_date}
Time: {registration.event.event_time}
"""

    qr = qrcode.make(qr_data)

    temp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    qr.save(temp.name)

    pdf.drawImage(
        ImageReader(temp.name),
        380,
        500,
        width=120,
        height=120
    )

    pdf.save()

    return response