from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    event_date = models.DateField()
    event_time = models.TimeField()
    description = models.TextField()

    image = models.ImageField(
        upload_to="events/",
        blank=True,
        null=True
    )

    seats = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="events"
    )

    def __str__(self):
        return self.title


class Registration(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE
    )

    registration_date = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ("user", "event")

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"