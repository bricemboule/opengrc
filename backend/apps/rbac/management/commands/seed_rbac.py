from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission
from apps.rbac.models import Role

ROLE_CONFIG = {
    "super_admin": {"name": "Super Admin", "permissions": "__all__"},
    "platform_admin": {"name": "Platform Admin", "permissions": [
        "view_organization", "add_organization", "change_organization",
        "view_project", "add_project", "change_project",
        "view_person", "add_person", "change_person",
    ]},
    "viewer": {"name": "Viewer", "permissions": ["view_organization", "view_project", "view_person"]},
}

class Command(BaseCommand):
    help = "Seed roles and permissions"

    def handle(self, *args, **options):
        all_permissions = Permission.objects.all()
        for code, config in ROLE_CONFIG.items():
            role, _ = Role.objects.get_or_create(code=code, defaults={"name": config["name"]})
            role.name = config["name"]
            role.save()
            if config["permissions"] == "__all__":
                role.permissions.set(all_permissions)
            else:
                perms = Permission.objects.filter(codename__in=config["permissions"])
                role.permissions.set(perms)
            self.stdout.write(self.style.SUCCESS(f"Role seeded: {role.name}"))
        self.stdout.write(self.style.SUCCESS("RBAC seeding completed."))
