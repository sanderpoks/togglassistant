from toggl_python.auth import TokenAuth
from toggl_python.entities.user import CurrentUser
from toggl_python.entities.workspace import Workspace
import datetime
from config import TOGGL_API_TOKEN

auth = TokenAuth(token=TOGGL_API_TOKEN)
workspace_api = Workspace(auth=auth)

def get_time_entries(start_date: str, end_date:str):
    """
    Fetch time entries from Toggl Track for the specified date range.

    Args:
        start_date (str): Start date in ISO 8601 format (YYYY-MM-DD).
        end_date (str): End date in ISO 8601 format (YYYY-MM-DD).

    Returns:
        list: A list of time entries.
    """
    try:
        # Fetch time entries using the TimeEntry entity
        time_entries = CurrentUser(auth=auth).get_time_entries(
            start_date=start_date,
            end_date=end_date
        )
        return time_entries
    except Exception as e:
        print(f"Error fetching time entries: {e}")
        return []

def fetch_workspaces():
    """
    Fetch a list of all workspaces for the authenticated user.

    Returns:
        list: A list of workspace objects.
    """
    try:
        return workspace_api.list()
    except Exception as e:
        print(f"Error fetching workspaces: {e}")
        return []

def fetch_projects(workspace_id):
    """
    Fetch all projects for a given workspace.

    Args:
        workspace_id (int): ID of the workspace.

    Returns:
        list: A list of project objects.
    """
    try:
        return workspace_api.get_projects(workspace_id=workspace_id)
    except Exception as e:
        print(f"Error fetching projects for workspace {workspace_id}: {e}")
        return []

def create_time_entry(workspace_id, description, start, duration=None, project_id=None, tags=None, billable=False):
    """
    Create a new time entry in Toggl Track.

    Args:
        workspace_id (int): ID of the workspace.
        description (str): Description of the time entry.
        start (str): Start time in ISO 8601 format.
        duration (int, optional): Duration in seconds. If None, the entry will be running.
        project_id (int, optional): Project ID to associate with the entry.
        tags (list, optional): List of tags for the entry.
        billable (bool, optional): Whether the entry is billable.

    Returns:
        dict: The created time entry details.
    """
    try:
        # Map parameters to align with Toggl API expectations
        time_entry_data = {
            "workspace_id": workspace_id,
            "start_datetime": start,  # Adjust to match `start_datetime`
            "created_with": "togglassistant",
            "description": description,
            "duration": duration if duration is not None else -1,  # -1 indicates a running timer
            "project_id": project_id,
            "tags": tags or [],
            "billable": billable,
        }

        # Pass parameters to the toggl-python API method
        response = workspace_api.create_time_entry(**time_entry_data)
        return response
    except Exception as e:
        print(f"Error creating time entry: {e}")
        return None
