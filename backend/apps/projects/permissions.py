from apps.core.action_permissions import ActionPermission

class ProjectPermission(ActionPermission):
    permission_map = {
        "list": "projects.view_project",
        "retrieve": "projects.view_project",
        "create": "projects.add_project",
        "update": "projects.change_project",
        "partial_update": "projects.change_project",
        "destroy": "projects.delete_project",
    }


class ActivityPermission(ActionPermission):
    permission_map = {
        "list": "projects.view_activity",
        "retrieve": "projects.view_activity",
        "create": "projects.add_activity",
        "update": "projects.change_activity",
        "partial_update": "projects.change_activity",
        "destroy": "projects.delete_activity",
    }


class TaskPermission(ActionPermission):
    permission_map = {
        "list": "projects.view_task",
        "retrieve": "projects.view_task",
        "create": "projects.add_task",
        "update": "projects.change_task",
        "partial_update": "projects.change_task",
        "destroy": "projects.delete_task",
    }
