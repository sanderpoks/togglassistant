from core.initialization import setup_workspace_and_projects
from core.time_entry_repository import TimeEntryRepository

from datetime import datetime, timezone

if __name__ == "__main__":
    setup_workspace_and_projects()
    repository = TimeEntryRepository()
    repository.download_entries("2025-01-10","2025-01-12")
    for i in repository.entries:
        print(i)