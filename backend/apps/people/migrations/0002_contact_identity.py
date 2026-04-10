# Generated manually on 2026-04-10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("org", "0002_site_facility"),
        ("people", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Contact",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("contact_type", models.CharField(default="SMS", max_length=32)),
                ("value", models.CharField(max_length=255)),
                ("label", models.CharField(blank=True, max_length=255)),
                ("priority", models.PositiveSmallIntegerField(default=1)),
                ("is_primary", models.BooleanField(default=False)),
                ("access_level", models.CharField(default="private", max_length=32)),
                ("comments", models.TextField(blank=True)),
                (
                    "created_by",
                    models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="created_%(class)ss", to=settings.AUTH_USER_MODEL),
                ),
                (
                    "organization",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="contacts", to="org.organization"),
                ),
                (
                    "person",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="contacts", to="people.person"),
                ),
                (
                    "updated_by",
                    models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="updated_%(class)ss", to=settings.AUTH_USER_MODEL),
                ),
            ],
            options={"ordering": ["priority", "-id"]},
        ),
        migrations.CreateModel(
            name="Identity",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("document_type", models.CharField(default="national_id", max_length=50)),
                ("description", models.CharField(blank=True, max_length=255)),
                ("document_number", models.CharField(blank=True, max_length=120)),
                ("valid_from", models.DateField(blank=True, null=True)),
                ("valid_until", models.DateField(blank=True, null=True)),
                ("issued_country", models.CharField(blank=True, max_length=4)),
                ("issued_place", models.CharField(blank=True, max_length=255)),
                ("issuing_authority", models.CharField(blank=True, max_length=255)),
                ("is_system_generated", models.BooleanField(default=False)),
                ("is_invalid", models.BooleanField(default=False)),
                ("comments", models.TextField(blank=True)),
                (
                    "created_by",
                    models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="created_%(class)ss", to=settings.AUTH_USER_MODEL),
                ),
                (
                    "organization",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="identities", to="org.organization"),
                ),
                (
                    "person",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="identities", to="people.person"),
                ),
                (
                    "updated_by",
                    models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="updated_%(class)ss", to=settings.AUTH_USER_MODEL),
                ),
            ],
            options={"ordering": ["-id"]},
        ),
    ]
