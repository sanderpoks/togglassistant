import json
from integration.toggl_api import fetch_workspaces, fetch_projects

def setup_workspace_and_projects():
    """
    Fetch workspace ID and project mappings from Toggl Track using the Integration Layer.
    Saves the data to config.json.

    Returns:
        dict: Configuration data with workspace ID and project mappings.
    """
    try:
        # Fetch workspaces via Integration Layer
        workspaces = fetch_workspaces()
        if not workspaces:
            raise ValueError("No workspaces found for this account.")
        
        # Use the first workspace (adjust if needed for multiple workspaces)
        workspace_id = workspaces[0].id
        print(f"Using Workspace ID: {workspace_id}")

        # Fetch projects via Integration Layer
        projects = fetch_projects(workspace_id=workspace_id)
        project_dict = {project.name: project.id for project in projects}

        print("Fetched Projects:")
        for name, project_id in project_dict.items():
            print(f"  {name}: {project_id}")

        # Save to config.json
        config_data = {
            "WORKSPACE_ID": workspace_id,
            "PROJECTS": project_dict,
        }
        save_to_config(config_data)
        return config_data
    except Exception as e:
        print(f"Error during setup: {e}")
        return {}

def save_to_config(data: dict):
    """
    Save workspace ID and project mappings to config.json.

    Args:
        data (dict): Configuration data to save.
    """
    try:
        with open("config.json", "w") as f:
            json.dump(data, f, indent=4)
        print("Configuration saved to config.json.")
    except Exception as e:
        print(f"Error saving configuration: {e}")

if __name__ == "__main__":
    config = setup_workspace_and_projects()
    if config:
        print("Initialization successful.")
        print("Saved Configuration:", config)
    else:
        print("Initialization failed.")