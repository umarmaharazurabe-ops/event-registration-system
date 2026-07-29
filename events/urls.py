from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),

    path('events/', views.event_list, name='events'),
    path('events/<int:id>/', views.event_detail, name='event_detail'),

    path(
        'register-event/<int:id>/',
        views.register_event,
        name='register_event'
    ),

    path(
        'my-registrations/',
        views.my_registrations,
        name='my_registrations'
    ),

    path('profile/', views.profile, name='profile'),

    path(
        'edit-profile/',
        views.edit_profile,
        name='edit_profile'
    ),

    path(
        'change-password/',
        views.change_password,
        name='change_password'
    ),

    path(
        'ticket/<int:id>/',
        views.download_ticket,
        name='download_ticket'
    ),

    path(
        'create/',
        views.create_event,
        name='create_event'
    ),

    path(
        'my-events/',
        views.my_events,
        name='my_events'
    ),

    path(
        'edit-event/<int:id>/',
        views.edit_event,
        name='edit_event'
    ),

    path(
        'delete-event/<int:id>/',
        views.delete_event,
        name='delete_event'
    ),
]