# Description
TogglAssistant is intended to be a CLI tool for TogglTrack time tracking (https://toggl.com/) related housekeeping and review.

It relies on Toggl API v9 (https://engineering.toggl.com/docs/) which it interfaces with using the toggl-python module (https://github.com/evrone/toggl-python)

# Functionality
- Downloading and reviewing Toggl time tracking data (including data filtering and visualisation)
- Performing housekeeping on Toggl data
    - Detecting and resolving overlapping time entries
    - Detecting and resolving untracked time
    - Grouping and unifying activity descriptions (to eliminate duplicates with different descriptions/details)
- Syncing changes back into TogglTrack
- Logging of all changes to the data

# Project architecture
The project is split into multiple interlocking layers

## Integration
The integration layer communicates with the TogglTrack API using the toggl-python module

## Interface
The interface layer provides the CLI for user display and input

## Core
The core layer deals with all the program logic, including local data caching, change tracking and housekeeping tasks

# Directory structure
toggl_tool/
├── core/
│   ├── data_processing.py
│   ├── validation.py
│   ├── initialization.py
│   └── __init__.py
├── interface/
│   ├── cli.py
│   ├── prompts.py
│   └── __init__.py
├── integration/
│   ├── toggl_api.py
│   └── __init__.py
├── config.json
├── config.py
├── main.py
└── requirements.txt