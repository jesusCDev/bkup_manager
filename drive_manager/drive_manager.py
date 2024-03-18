import json
from pathlib import Path
from typing import List

from drive_manager.drive import Drive
import constants


class DriveManager:
    backup_drive_data = None
    drive_list        = []
    
    def __init__(self, script_dir: Path):
        json_path  = script_dir / 'data/drives.json'

        with json_path.open() as drives_file:
            self.backup_drive_data = json.load(drives_file)
            
        self.drive_list = self.get_list_of_backup_drives()
    
    def get_list_of_backup_drives(self) -> List[Drive]:
        return [
            Drive(
                drive[constants.DISK_NAME_KEY], 
                drive[constants.DISK_LOCATION_KEY], 
                drive[constants.BACKUP_FOLDER_NAME_KEY],
                drive[constants.BACKUP_TYPE_KEY], 
                drive[constants.PORTAL_IGNORE_FOLDER_LIST_KEY], 
                drive[constants.LOCAL_IGNORE_FOLDER_LIST_KEY]
            ) for drive in self.backup_drive_data[constants.BACKUP_DRIVES_KEY]
        ]
    
    def get_drives_for_backup(self, drives_to_backup: str = constants.OPTION_ALL) -> List[Drive]:
        if drives_to_backup == constants.OPTION_ALL:
            return self.drive_list
        else:
            return [self.find_drive_by_name(drives_to_backup)]

    def find_drive_by_name(self, drive_name: str) -> Drive:
        for drive in self.drive_list:
            if drive.drive_name.lower() == drive_name.lower():
                return drive

    def get_backup_directory_path(self, backup_to_local_drive: bool = True) -> Path:
        if backup_to_local_drive:
            return Path(self.backup_drive_data[constants.LOCAL_BACKUP_DRIVE_KEY][constants.BACKUP_DRIVES_LOCATION_KEY])
        else:
            return Path(self.backup_drive_data[constants.PORTAL_BACKUP_DRIVE_KEY][constants.BACKUP_DRIVES_LOCATION_KEY])