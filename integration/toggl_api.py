from toggl_python.auth import TokenAuth
from toggl_python.entities.user import CurrentUser
from toggl_python.entities.workspace import Workspace
import datetime
from config import TOGGL_API_TOKEN

auth = TokenAuth(token=TOGGL_API_TOKEN)
workspace_api = Workspace(auth=auth)

def get_time_entries(start_datetime: str, end_datetime: str):
    """
    Fetch time entries from Toggl Track for the specified date-time range.

    Args:
        start_datetime (str): Start date-time in ISO 8601 format (e.g., '2025-01-11T08:00:00Z').
        end_datetime (str): End date-time in ISO 8601 format (e.g., '2025-01-11T18:00:00Z').

    Returns:
        list: A list of time entries.
    """
    try:
        time_entries = CurrentUser(auth=auth).get_time_entries(
            start_date=start_datetime,  # Can include both date and time
            end_date=end_datetime       # Can include both date and time
        )
        return time_entries
    except Exception as e:
        print(f"Error fetching time entries: {e}")
        return []

    
def get_running_entry():
    """
    Fetch the currently running time entry (if any).

    Returns:
        dict: Running time entry details or None if no entry is running.
    """
    try:
        # Use the built-in method to fetch the current time entry
        running_entry = CurrentUser(auth=auth).get_current_time_entry()
        return running_entry
    except Exception as e:
        print(f"Error fetching running time entry: {e}")
        return None

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

def update_time_entry(workspace_id, entry_id, description=None, start=None, stop=None, project_id=None, tags=None):
    """
    Update an existing time entry in Toggl Track.

    Args:
        workspace_id (int): Workspace ID where the entry exists.
        entry_id (int): The ID of the time entry to update.
        description (str, optional): New description.
        start (str, optional): New start time in ISO 8601 format.
        stop (str, optional): New stop time in ISO 8601 format.
        project_id (int, optional): New project ID.
        tags (list, optional): New tags.

    Returns:
        dict: Updated time entry details.
    """
    try:
        update_data = {
            "description": description,
            "start": start,
            "stop": stop,
            "project_id": project_id,
            "tags": tags or [],
        }
        # Remove None values to avoid sending unnecessary fields
        update_data = {k: v for k, v in update_data.items() if v is not None}

        response = workspace_api.update_time_entry(
            workspace_id=workspace_id,
            time_entry_id=entry_id,
            **update_data
        )
        return response
    except Exception as e:
        print(f"Error updating time entry: {e}")
        return None

def delete_time_entry(workspace_id, entry_id):
    """
    Delete a time entry in Toggl Track.

    Args:
        workspace_id (int): Workspace ID where the entry exists.
        entry_id (int): The ID of the time entry to delete.

    Returns:
        bool: True if the entry was deleted successfully, False otherwise.
    """
    try:
        success = workspace_api.delete_time_entry(workspace_id=workspace_id, time_entry_id=entry_id)
        return success
    except Exception as e:
        print(f"Error deleting time entry: {e}")
        return False
