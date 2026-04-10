from apps.core.action_permissions import ActionPermission

class PersonPermission(ActionPermission):
    permission_map = {
        "list": "people.view_person",
        "retrieve": "people.view_person",
        "create": "people.add_person",
        "update": "people.change_person",
        "partial_update": "people.change_person",
        "destroy": "people.delete_person",
    }


class ContactPermission(ActionPermission):
    permission_map = {
        "list": "people.view_contact",
        "retrieve": "people.view_contact",
        "create": "people.add_contact",
        "update": "people.change_contact",
        "partial_update": "people.change_contact",
        "destroy": "people.delete_contact",
    }


class IdentityPermission(ActionPermission):
    permission_map = {
        "list": "people.view_identity",
        "retrieve": "people.view_identity",
        "create": "people.add_identity",
        "update": "people.change_identity",
        "partial_update": "people.change_identity",
        "destroy": "people.delete_identity",
    }
