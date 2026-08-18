# Generated manually for the initial MixMidas booking model.
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Booking",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254)),
                ("service", models.CharField(choices=[("Mixing", "Mixing"), ("Mastering", "Mastering"), ("Vocal Recording", "Vocal Recording"), ("Vocal Editing", "Vocal Editing")], max_length=30)),
                ("date", models.DateField()),
                ("start_time", models.TimeField()),
                ("duration_hours", models.PositiveSmallIntegerField()),
                ("project_details", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
