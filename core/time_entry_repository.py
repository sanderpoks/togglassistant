import json
from core.time_entry import TimeEntry
from integration.toggl_api import get_time_entries
from datetime import datetime, timedelta

class TimeEntryRepository:
    def __init__(self, file_path="repository.json"):
        self.file_path = file_path
        self.entries = []
        self.load_entries()

    from datetime import datetime

    def load_entries(self):
        """Load entries from the file into memory."""
        try:
            with open(self.file_path, "r") as f:
                data = json.load(f)
                self.entries = [
                    TimeEntry(
                        id=entry["id"],
                        workspace_id=entry["workspace_id"],
                        start=datetime.fromisoformat(entry["start"]) if entry["start"] else None,
                        duration=entry["duration"],
                        description=entry.get("description"),
                        stop=datetime.fromisoformat(entry["stop"]) if entry.get("stop") else None,
                        project_id=entry.get("project_id"),
                        tags=entry.get("tags", []),
                        billable=entry.get("billable", False),
                    )
                    for entry in data
                ]
        except FileNotFoundError:
            print(f"{self.file_path} not found. Starting with an empty repository.")
            self.entries = []
        except json.JSONDecodeError:
            print(f"Invalid JSON in {self.file_path}. Starting with an empty repository.")
            self.entries = []
        except Exception as e:
            print(f"Unexpected error loading entries: {e}")
            self.entries = []

    
    def download_entries(self, start_datetime: str, end_datetime: str):
        """
        Download time entries from TogglTrack and store them in the repository.

        Args:
            start_datetime (str): Start time in ISO 8601 format (e.g., "2025-01-01T00:00:00Z").
            end_datetime (str): End time in ISO 8601 format (e.g., "2025-01-02T00:00:00Z").
        """
        raw_entries = get_time_entries(start_datetime, end_datetime)
        for raw_entry in raw_entries:
            try:
                time_entry = TimeEntry(
                    id=raw_entry.id,
                    workspace_id=raw_entry.workspace_id,
                    start=raw_entry.start,
                    duration=raw_entry.duration,
                    description=raw_entry.description,
                    stop=raw_entry.stop,
                    project_id=raw_entry.project_id,
                    tags=raw_entry.tags,
                    billable=raw_entry.billable,
                )
                self.entries.append(time_entry)
            except Exception as e:
                print(f"Error processing entry {raw_entry.id if hasattr(raw_entry, 'id') else 'unknown'}: {e}")

        self.save_entries()



    def save_entries(self):
        """Save the current state of entries back to the file."""
        with open(self.file_path, "w") as f:
            json.dump([entry.to_dict() for entry in self.entries], f, indent=4)

    def add_entry(self, time_entry):
        """Add a new time entry."""
        time_entry.state = "new"
        self.entries.append(time_entry)
        self.save_entries()

    def update_entry(self, entry_id, updated_data):
        """Update an existing time entry."""
        for entry in self.entries:
            if entry.id == entry_id:
                entry.update(updated_data)
                entry.state = "modified"
                break
        self.save_entries()

    def delete_entry(self, entry_id):
        """Mark an entry for deletion."""
        for entry in self.entries:
            if entry.id == entry_id:
                entry.state = "deleted"
                break
        self.save_entries()

    def get_entries(self, state=None):
        """Retrieve all entries, optionally filtered by state."""
        if state:
            return [entry for entry in self.entries if entry.state == state]
        return self.entries

    def get_changes(self):
        """Retrieve new, modified, and deleted entries."""
        new_entries = self.get_entries(state="new")
        modified_entries = self.get_entries(state="modified")
        deleted_entries = self.get_entries(state="deleted")
        return new_entries, modified_entries, deleted_entries

    def sync_with_toggl(self, toggl_api):
        """Sync changes with TogglTrack."""
        new, modified, deleted = self.get_changes()
        # Sync logic (calling API functions)
        for entry in new:
            toggl_api.create_time_entry(entry.to_api_format())
        for entry in modified:
            toggl_api.update_time_entry(entry.id, entry.to_api_format())
        for entry in deleted:
            toggl_api.delete_time_entry(entry.id)
        # Reset states after syncing
        for entry in self.entries:
            if entry.state in {"new", "modified"}:
                entry.state = "unchanged"
        self.entries = [e for e in self.entries if e.state != "deleted"]
        self.save_entries()
