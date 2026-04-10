from apps.core.action_permissions import ActionPermission

class OrganizationPermission(ActionPermission):
    permission_map = {
        "list": "org.view_organization",
        "retrieve": "org.view_organization",
        "create": "org.add_organization",
        "update": "org.change_organization",
        "partial_update": "org.change_organization",
        "destroy": "org.delete_organization",
    }


class SitePermission(ActionPermission):
    permission_map = {
        "list": "org.view_site",
        "retrieve": "org.view_site",
        "create": "org.add_site",
        "update": "org.change_site",
        "partial_update": "org.change_site",
        "destroy": "org.delete_site",
    }


class FacilityPermission(ActionPermission):
    permission_map = {
        "list": "org.view_facility",
        "retrieve": "org.view_facility",
        "create": "org.add_facility",
        "update": "org.change_facility",
        "partial_update": "org.change_facility",
        "destroy": "org.delete_facility",
    }


class OrganizationTypePermission(ActionPermission):
    permission_map = {
        "list": "org.view_organizationtype",
        "retrieve": "org.view_organizationtype",
        "create": "org.add_organizationtype",
        "update": "org.change_organizationtype",
        "partial_update": "org.change_organizationtype",
        "destroy": "org.delete_organizationtype",
    }


class OfficeTypePermission(ActionPermission):
    permission_map = {
        "list": "org.view_officetype",
        "retrieve": "org.view_officetype",
        "create": "org.add_officetype",
        "update": "org.change_officetype",
        "partial_update": "org.change_officetype",
        "destroy": "org.delete_officetype",
    }


class FacilityTypePermission(ActionPermission):
    permission_map = {
        "list": "org.view_facilitytype",
        "retrieve": "org.view_facilitytype",
        "create": "org.add_facilitytype",
        "update": "org.change_facilitytype",
        "partial_update": "org.change_facilitytype",
        "destroy": "org.delete_facilitytype",
    }
