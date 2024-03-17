# Backup Manager

## Overview
This project automates the backup of files and directories to specific locations, supporting both local and portal backups. It includes comprehensive logging capabilities to facilitate monitoring and debugging. Key features include the use of `rsync` for efficient file synchronization, the ability to run in both production and test modes, and notifications on backup completion.

## Features
- Selective backup based on user-defined criteria.
- Support for local and portal backup destinations.
- Detailed logging with `logging` module for easy monitoring.
- Efficient file synchronization with `rsync`.
- Notification system for backup completion in production mode.
- Configurable for test and production environments.

## Requirements
- Python 3.x
- `colorama` library
- `rsync` for file synchronization
- `notify-desktop` for desktop notifications (Linux only)

## Setup Instructions

1. **Clone the Repository**: Download the code to your local machine.
2. **Install Dependencies**: Run `pip install -r requirements.txt` to install required Python libraries.
3. **Ensure System Requirements**: Make sure `rsync` and `notify-desktop` (Linux) are installed on your system.

### Configuring Drives for Backup

Create a `drives.json` file in the `data` directory with the following structure:

```json
{
    "backup_drives": [
        {
            "drive_name": "example_drive",
            "drive_location": "/path/to/example_drive",
            "backup_folder_name": "example_backup",
            "backup_type": "local",
            "portal_ignore_folder_list": ["temp", "node_modules"],
            "local_ignore_folder_list": ["temp", "node_modules"]
        }
    ],
    "portal_backup_drive": {
        "drive_name": "portal_drive",
        "drive_location": "/path/to/portal_drive",
        "backup_folder_name": "portal_backup"
    },
    "local_backup_drive": {
        "drive_name": "local_drive",
        "drive_location": "/path/to/local_drive",
        "backup_folder_name": "local_backup"
    }
}
```

- Replace placeholders (e.g., `<drive_name>`, `<drive_location>`) with your actual data.
- `backup_type` can be `both`, `portal`, or `local`.
- The ignore lists allow excluding specific folders from backups.

## Usage

Execute the script with the following command-line arguments:

```
python main.py -l <location> -d <drive> [-p] [-t]
```

Options:
- `-l`, `--location`: The backup location (`local` or `portal`).
- `-d`, `--drive`: The drive to back up (`all` or a specific backup folder name).
- `-p`, `--production`: Run in production mode (optional).
- `-t`, `--test`: Run in test mode for verbose logging (optional).

Example:
```
python main.py -l local -d example_backup -p
```

This command would initiate a backup of `example_backup` to the local backup location in production mode.

## Contributing
Contributions are welcome! Please feel free to submit pull requests or open issues for any improvements or bug fixes.