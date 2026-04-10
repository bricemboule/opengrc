import factory
from apps.org.models import Organization

class OrganizationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Organization

    name = factory.Sequence(lambda n: f"Organization {n}")
    code = factory.Sequence(lambda n: f"ORG{n:03d}")
    is_active = True
