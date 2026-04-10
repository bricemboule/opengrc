from django.core.management.base import BaseCommand, CommandError
from apps.accounts.models import User
from apps.rbac.models import Role

class Command(BaseCommand):
    help = "Assign role to user"

    def add_arguments(self, parser):
        parser.add_argument("email", type=str)
        parser.add_argument("role_code", type=str)

    def handle(self, *args, **options):
        email = options["email"]
        role_code = options["role_code"]
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise CommandError("User not found")
        try:
            role = Role.objects.get(code=role_code)
        except Role.DoesNotExist:
            raise CommandError("Role not found")
        user.roles.add(role)
        self.stdout.write(self.style.SUCCESS(f"{role.code} assigned to {user.email}"))
