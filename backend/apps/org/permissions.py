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
