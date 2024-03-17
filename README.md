# Project Title

## Setup

### drives.json

Create a `drives.json` file in the `drive_manager` directory with the following format:

```json
{
    "backup_drives" : [
        {
            "drive_name"               : "<drive_name>",
            "drive_location"           : "<drive_location>",
            "backup_folder_name"       : "<backup_folder_name>",
            "backup_type"              : "<backup_type>",
            "portal_ignore_folder_list": ["<folder_to_ignore_1>", "<folder_to_ignore_2>", "..."],
            "local_ignore_folder_list" : ["<folder_to_ignore_1>", "<folder_to_ignore_2>", "..."]
        },
        // Add more drives as needed
    ],
    "portal_backup_drive": {
        "drive_name"        : "<drive_name>",
        "drive_location"    : "<drive_location>",
        "backup_folder_name": "<backup_folder_name>"
    },
    "local_backup_drive": {
        "drive_name"        : "<drive_name>",
        "drive_location"    : "<drive_location>",
        "backup_folder_name": "<backup_folder_name>"
    }
}
```

Replace <drive_name>, <drive_location>, <backup_folder_name>, <backup_type>, and <folder_to_ignore> with your actual values.

<backup_type> can be "both", "portal", or "local".

<folder_to_ignore> is a folder you want to exclude from the backup. You can add as many folders as you want to the ignore lists.

# Running the Project
To run the project, use the following command:

Command line arguments:

-l, --location: Required. The backup location. Choices are 'local' or 'portal'.
-d, --drive: Required. The drive to backup. Choices are 'all' or any of the backup folder names specified in drives.json.
-p, --production: Optional. If specified, the program runs in production mode.
-t, --test: Optional. If specified, the program runs in test mode.