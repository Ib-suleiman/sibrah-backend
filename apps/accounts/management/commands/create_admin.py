# from django.core.management.base import BaseCommand
# from django.contrib.auth import get_user_model
# import os

# class Command(BaseCommand):
#     help = "Create admin user from environment variables"

#     def handle(self, *args, **kwargs):
#         User = get_user_model()

#         username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
#         email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
#         password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

#         if not username or not password:
#             self.stdout.write(self.style.ERROR("Missing env variables"))
#             return

#         if not User.objects.filter(username=username).exists():
#             User.objects.create_superuser(
#                 username=username,
#                 email=email,
#                 password=password
#             )
#             self.stdout.write(self.style.SUCCESS("Admin created"))
#         else:
#             self.stdout.write("Admin already exists")


from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = "Create or update admin user from environment variables"

    def handle(self, *args, **kwargs):
        User = get_user_model()

        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

        if not username or not password:
            self.stdout.write(self.style.ERROR("Missing environment variables"))
            return

        user, created = User.objects.get_or_create(
            username=username,
            defaults={"email": email},
        )

        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.set_password(password)
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS("Admin created"))
        else:
            self.stdout.write(self.style.SUCCESS("Admin updated"))