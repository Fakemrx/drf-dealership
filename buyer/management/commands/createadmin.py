"""Management command to create Django-superuser."""
import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    """Command class to create Django-superuser."""

    help = "Creates super user instance using .env variables"

    def add_arguments(self, parser):
        parser.add_argument("username", nargs="?", type=str)
        parser.add_argument("password", nargs="?", type=str)

    def handle(self, *args, **options):
        if options["username"] is None:
            username = os.environ.get("DJANGO_SUPERUSER_USERNAME", default="Admin")
        else:
            username = options["username"]
        if options["password"] is None:
            password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", default="1234")
        else:
            password = options["password"]
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "is_staff": True,
                "is_superuser": True,
            },
        )
        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f"Admin created! Username: {username}, Password: {password}"
                )
            )
        else:
            self.stdout.write(self.style.ERROR(f"User '{username}' already exists!"))
