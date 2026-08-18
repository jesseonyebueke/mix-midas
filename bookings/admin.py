from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("name", "service", "date", "start_time", "duration_hours", "total_cost", "email", "created_at")
    list_filter = ("service", "date")
    search_fields = ("name", "email")
    ordering = ("date", "start_time")
