# Generated manually on 2026-04-10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("volunteers", "0001_initial"),
        ("hr", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="staff",
            name="contract_end_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name="Certificate",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("code", models.CharField(max_length=80, unique=True)),
                ("name", models.CharField(max_length=255)),
                ("status", models.CharField(default="draft", max_length=50)),
                ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="created_%(class)ss", to=settings.AUTH_USER_MODEL)),
                ("updated_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="updated_%(class)ss", to=settings.AUTH_USER_MODEL)),
                ("organization", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="certificate_hr", to="org.organization")),
            ],
            options={"ordering": ["-id"]},
        ),
        migrations.CreateModel(
            name="Team",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("code", models.CharField(max_length=80, unique=True)),
                ("name", models.CharField(max_length=255)),
                ("status", models.CharField(default="active", max_length=50)),
                ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="created_%(class)ss", to=settings.AUTH_USER_MODEL)),
                ("updated_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="updated_%(class)ss", to=settings.AUTH_USER_MODEL)),
                ("organization", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="team_hr", to="org.organization")),
            ],
            options={"ordering": ["-id"]},
        ),
        migrations.CreateModel(
            name="TrainingCourse",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("code", models.CharField(max_length=80, unique=True)),
                ("name", models.CharField(max_length=255)),
                ("status", models.CharField(default="draft", max_length=50)),
                ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="created_%(class)ss", to=settings.AUTH_USER_MODEL)),
                ("updated_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="updated_%(class)ss", to=settings.AUTH_USER_MODEL)),
                ("organization", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="trainingcourse_hr", to="org.organization")),
            ],
            options={"ordering": ["-id"]},
        ),
        migrations.CreateModel(
            name="TeamMember",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("role", models.CharField(blank=True, max_length=120)),
                ("status", models.CharField(default="active", max_length=50)),
                ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="created_%(class)ss", to=settings.AUTH_USER_MODEL)),
                ("updated_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="updated_%(class)ss", to=settings.AUTH_USER_MODEL)),
                ("organization", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="teammember_hr", to="org.organization")),
                ("staff", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="team_memberships", to="hr.staff")),
                ("team", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="members", to="hr.team")),
            ],
            options={"ordering": ["-id"]},
        ),
        migrations.CreateModel(
            name="StaffSkill",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("proficiency", models.CharField(blank=True, max_length=80)),
                ("status", models.CharField(default="active", max_length=50)),
                ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="created_%(class)ss", to=settings.AUTH_USER_MODEL)),
                ("updated_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="updated_%(class)ss", to=settings.AUTH_USER_MODEL)),
                ("organization", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="staffskill_hr", to="org.organization")),
                ("skill", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="staff_links", to="volunteers.skill")),
                ("staff", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="skills", to="hr.staff")),
            ],
            options={"ordering": ["-id"]},
        ),
        migrations.CreateModel(
            name="TrainingEvent",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("code", models.CharField(max_length=80, unique=True)),
                ("name", models.CharField(max_length=255)),
                ("start_date", models.DateField(blank=True, null=True)),
                ("end_date", models.DateField(blank=True, null=True)),
                ("status", models.CharField(default="planned", max_length=50)),
                ("certificate", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="training_events", to="hr.certificate")),
                ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="created_%(class)ss", to=settings.AUTH_USER_MODEL)),
                ("organization", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="trainingevent_hr", to="org.organization")),
                ("training_course", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="events", to="hr.trainingcourse")),
                ("updated_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="updated_%(class)ss", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-id"]},
        ),
        migrations.CreateModel(
            name="TrainingParticipant",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("completion_status", models.CharField(default="registered", max_length=50)),
                ("score", models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ("certificate_awarded", models.BooleanField(default=False)),
                ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="created_%(class)ss", to=settings.AUTH_USER_MODEL)),
                ("organization", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="trainingparticipant_hr", to="org.organization")),
                ("staff", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="training_participations", to="hr.staff")),
                ("training_event", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="participants", to="hr.trainingevent")),
                ("updated_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="updated_%(class)ss", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-id"]},
        ),
    ]
