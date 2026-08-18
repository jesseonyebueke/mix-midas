import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Creates or updates an admin account from environment variables."

    def handle(self, *args, **options):
        username = os.getenv("ADMIN_USERNAME")
        email = os.getenv("ADMIN_EMAIL")
        password = os.getenv("ADMIN_PASSWORD")
        if not all((username, email, password)):
            self.stdout.write("Admin bootstrap skipped: ADMIN_USERNAME, ADMIN_EMAIL, and ADMIN_PASSWORD are not all set.")
            return

        user_model = get_user_model()
        user, _ = user_model.objects.get_or_create(username=username)
        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()
        self.stdout.write(self.style.SUCCESS(f"Admin account ready: {username}"))
