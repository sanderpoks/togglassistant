import json
from datetime import datetime, timezone
from integration.toggl_api import create_time_entry

# Helper functions for configuration handling
def _get_workspace_id():
    """
    Retrieve the default workspace ID from config.json.
    """
    with open("config.json", "r") as f:
        config = json.load(f)
    workspace_id = config.get("WORKSPACE_ID")
    if not workspace_id:
        raise ValueError("Workspace ID not found in config.json.")
    return workspace_id


def _get_project_id(project_name):
    """
    Resolve the project name to its ID using config.json.

    Args:
        project_name (str): The name of the project.

    Returns:
        int: The project ID.
    """
    with open("config.json", "r") as f:
        config = json.load(f)
    projects = config.get("PROJECTS", {})
    project_id = projects.get(project_name)
    if not project_id:
        raise ValueError(f"Project '{project_name}' not found in config.json.")
    return project_id

# Main functionality
def add_time_entry(description, start=None, project_name=None, duration=None, tags=None, billable=False):
    """
    Add a new time entry using project name instead of project ID.
    """
    try:
        workspace_id = _get_workspace_id()
        project_id = _get_project_id(project_name) if project_name else None

        # Default start time to current time if not provided
        if not start:
            start = datetime.now(timezone.utc)
        start_iso = start.isoformat()

        # Call the API to create the time entry
        return create_time_entry(
            workspace_id=workspace_id,
            description=description,
            start=start_iso,
            duration=duration,
            project_id=project_id,
            tags=tags,
            billable=billable
        )
    except Exception as e:
        print(f"Error adding time entry: {e}")
        return None
