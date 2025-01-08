from core.initialization import setup_workspace_and_projects
from integration.toggl_api import get_running_entry
from core.data_processing import add_time_entry, _get_workspace_id

from datetime import datetime, timezone

if __name__ == "__main__":
    setup_workspace_and_projects()

    # Fetch the currently running time entry
    workspace_id = _get_workspace_id()  # Automatically get workspace ID from config

    running_entry = get_running_entry()

    if running_entry:
        print("Running Time Entry:", running_entry)
    else:
        print("No running time entry found.")
