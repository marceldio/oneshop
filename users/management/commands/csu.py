from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):
    help = "Создает суперпользователя с указанным email и паролем"

    def add_arguments(self, parser):
        parser.add_argument("--email", type=str, help="Email суперпользователя", default="admin@example.com")
        parser.add_argument("--password", type=str, help="Пароль суперпользователя", default="0000")

    def handle(self, *args, **options):
        email = options["email"]
        password = options["password"]

        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING(f"Суперпользователь с email {email} уже существует."))
        else:
            user = User.objects.create_superuser(email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f"Суперпользователь {email} успешно создан!"))
