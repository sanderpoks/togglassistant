from datetime import datetime, timedelta
from typing import Optional, List

class TimeEntry:
    def __init__(
        self,
        id: int,
        workspace_id: int,
        start: datetime,
        duration: int,
        description: Optional[str] = None,
        stop: Optional[datetime] = None,
        project_id: Optional[int] = None,
        tags: Optional[List[str]] = None,
        billable: Optional[bool] = False
    ):
        # Validation
        if not isinstance(id, int):
            raise ValueError("id must be an integer")
        if not isinstance(workspace_id, int):
            raise ValueError("workspace_id must be an integer")
        if not isinstance(start, datetime):
            raise ValueError("start must be a datetime object")
        if not isinstance(duration, int):
            raise ValueError("duration must be an integer")
        if stop is not None and not isinstance(stop, datetime):
            raise ValueError("stop must be a datetime object or None")
        if description is not None and not isinstance(description, str):
            raise ValueError("description must be a string or None")
        if project_id is not None and not isinstance(project_id, int):
            raise ValueError("project_id must be an integer or None")
        if tags is not None:
            if not isinstance(tags, list) or not all(isinstance(tag, str) for tag in tags):
                raise ValueError("tags must be a list of strings or None")
        if billable is not None and not isinstance(billable, bool):
            raise ValueError("billable must be a boolean or None")
        
        self.id = id
        self.workspace_id = workspace_id
        self.start = start
        self.duration = duration
        self.description = description
        self.stop = stop
        self.project_id = project_id
        self.tags = tags or []
        self.billable = billable


    def calculate_stop(self) -> Optional[datetime]:
        """
        Calculate the stop time based on the start time and duration.
        If the timer is running (duration == -1), return None.
        """
        if self.is_running():
            return None  # Running timer has no stop time
        return self.start + timedelta(seconds=self.duration)


    def is_running(self) -> bool:
        return self.duration < 0

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "workspace_id": self.workspace_id,
            "start": self.start.isoformat() if self.start else None,
            "stop": self.stop.isoformat() if self.stop else None,
            "duration": self.duration,
            "description": self.description,
            "project_id": self.project_id,
            "tags": self.tags,
            "billable": self.billable,
        }

    def __str__(self):
        if self.is_running():
            stop_time = "Running"  # Display "Running" for ongoing entries
        else:
            stop_time = self.calculate_stop()
        return f"[{self.id}] {self.start} - {stop_time} | {self.description or 'No description'}"


    def print_entry(self):
        print(f"{self.id}\t{self.start}-{self.calculate_stop()}\t{self.description}")
