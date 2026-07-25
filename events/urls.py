from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path("events/", views.event_list, name="events"),
    path("events/<int:id>/", views.event_detail, name="event_detail"),
    path("register-event/<int:id>/",views.register_event,name="register_event"),
    path("my-registrations/",views.my_registrations,name="my_registrations"),
    path( "logout/",views.logout_view,name="logout"),
    path("profile/",views.profile,name="profile"),
    path('events/<int:id>/',views.event_detail,name='event_detail'),
    path(
    'register-event/<int:id>/',
    views.register_event,
    name='register_event'
),
path(
    "my-registrations/",
    views.my_registrations,
    name="my_registrations"
),
path(
    "edit-profile/",
    views.edit_profile,
    name="edit_profile"
),
path(
    "change-password/",
    views.change_password,
    name="change_password"
),
path(
    "ticket/<int:id>/",
    views.download_ticket,
    name="download_ticket",
),
]