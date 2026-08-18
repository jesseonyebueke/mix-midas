from datetime import datetime, time, timedelta
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Booking


class BookingForm(forms.ModelForm):
    start_time = forms.ChoiceField(choices=[])
    duration_hours = forms.ChoiceField(choices=[])

    class Meta:
        model = Booking
        fields = ["name", "email", "service", "date", "start_time", "duration_hours", "project_details"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "project_details": forms.Textarea(attrs={"rows": 4, "placeholder": "A few words about your sound, references, or goals…"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["service"].empty_label = "Choose a service"
        self.fields["start_time"].choices = [(f"{hour:02d}:00", self.label_for_hour(hour)) for hour in range(10, 18)]
        submitted_hour = self.data.get("start_time", "")
        try:
            hour = int(submitted_hour.split(":")[0])
        except (ValueError, IndexError):
            hour = 10
        self.fields["duration_hours"].choices = [(str(hours), f"{hours} hour{'s' if hours > 1 else ''}") for hours in range(1, 19 - hour)]
        self.fields["start_time"].widget.attrs["data-start-time"] = "true"
        self.fields["duration_hours"].widget.attrs["data-duration"] = "true"

    @staticmethod
    def label_for_hour(hour):
        suffix = "AM" if hour < 12 else "PM"
        display = hour if hour <= 12 else hour - 12
        return f"{display}:00 {suffix}"

    def clean_start_time(self):
        value = self.cleaned_data["start_time"]
        hour = int(value.split(":")[0])
        if not 10 <= hour < 18:
            raise ValidationError("Sessions can only start between 10:00 AM and 5:00 PM.")
        return time(hour, 0)

    def clean(self):
        cleaned = super().clean()
        start = cleaned.get("start_time")
        duration = cleaned.get("duration_hours")
        booking_date = cleaned.get("date")
        if booking_date and booking_date < timezone.localdate():
            self.add_error("date", "Please choose today or a future date.")
        if start and duration:
            duration = int(duration)
            if start.hour + duration > 18:
                self.add_error("duration_hours", "Your session must finish by 6:00 PM.")
            cleaned["duration_hours"] = duration
            if booking_date:
                new_start = datetime.combine(booking_date, start)
                new_end = new_start + timedelta(hours=duration)
                for existing in Booking.objects.filter(date=booking_date):
                    existing_start = datetime.combine(existing.date, existing.start_time)
                    existing_end = existing_start + timedelta(hours=existing.duration_hours)
                    if new_start < existing_end and new_end > existing_start:
                        self.add_error("start_time", "That time overlaps an existing session. Please choose another time.")
                        break
        return cleaned
