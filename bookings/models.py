from django.db import models


class Booking(models.Model):
    class Service(models.TextChoices):
        MIXING = "Mixing", "Mixing"
        MASTERING = "Mastering", "Mastering"
        VOCAL_RECORDING = "Vocal Recording", "Vocal Recording"
        VOCAL_EDITING = "Vocal Editing", "Vocal Editing"

    name = models.CharField(max_length=100)
    email = models.EmailField()
    service = models.CharField(max_length=30, choices=Service.choices)
    date = models.DateField()
    start_time = models.TimeField()
    duration_hours = models.PositiveSmallIntegerField()
    project_details = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_cost(self):
        return self.duration_hours * 10000

    def __str__(self):
        return f"{self.name} — {self.service} ({self.date})"
