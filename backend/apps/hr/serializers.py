from rest_framework import serializers
from .models import (
    Certificate,
    Department,
    JobTitle,
    Staff,
    StaffSkill,
    Team,
    TeamMember,
    TrainingCourse,
    TrainingEvent,
    TrainingParticipant,
)


class DepartmentSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(source="organization.name", read_only=True)

    class Meta:
        model = Department
        fields = "__all__"


class JobTitleSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(source="organization.name", read_only=True)

    class Meta:
        model = JobTitle
        fields = "__all__"


class StaffSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(source="organization.name", read_only=True)
    person_name = serializers.SerializerMethodField()
    department_name = serializers.CharField(source="department.name", read_only=True)
    job_title_name = serializers.CharField(source="job_title.name", read_only=True)

    class Meta:
        model = Staff
        fields = "__all__"

    def get_person_name(self, obj):
        return f"{obj.person.first_name} {obj.person.last_name}".strip()


class TeamSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(source="organization.name", read_only=True)

    class Meta:
        model = Team
        fields = "__all__"


class TeamMemberSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(source="organization.name", read_only=True)
    team_name = serializers.CharField(source="team.name", read_only=True)
    staff_name = serializers.CharField(source="staff.name", read_only=True)

    class Meta:
        model = TeamMember
        fields = "__all__"


class StaffSkillSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(source="organization.name", read_only=True)
    staff_name = serializers.CharField(source="staff.name", read_only=True)
    skill_name = serializers.CharField(source="skill.name", read_only=True)

    class Meta:
        model = StaffSkill
        fields = "__all__"


class TrainingCourseSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(source="organization.name", read_only=True)

    class Meta:
        model = TrainingCourse
        fields = "__all__"


class CertificateSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(source="organization.name", read_only=True)

    class Meta:
        model = Certificate
        fields = "__all__"


class TrainingEventSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(source="organization.name", read_only=True)
    training_course_name = serializers.CharField(source="training_course.name", read_only=True)
    certificate_name = serializers.CharField(source="certificate.name", read_only=True)

    class Meta:
        model = TrainingEvent
        fields = "__all__"


class TrainingParticipantSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(source="organization.name", read_only=True)
    training_event_name = serializers.CharField(source="training_event.name", read_only=True)
    staff_name = serializers.CharField(source="staff.name", read_only=True)

    class Meta:
        model = TrainingParticipant
        fields = "__all__"
