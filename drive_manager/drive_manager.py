from drive_manager.drive import Drive
import json
from pathlib import Path
from typing import List


class DriveManager:
    data       = None
    drive_list = []
    
    def __init__(self, script_dir: Path):
        json_path  = script_dir / 'data/drives.json'

        with json_path.open() as drives_file:
            self.data = json.load(drives_file)
            
        self.drive_list = self.get_list_of_backup_drives()
    
    def get_list_of_backup_drives(self) -> List[Drive]:
        return [
            Drive(
                drive['drive_name'], 
                drive['drive_location'], 
                drive['backup_folder_name'],
                drive['backup_type'], 
                drive['portal_ignore_folder_list'], 
                drive['local_ignore_folder_list']
            ) 
            
            for drive in self.data['backup_drives']
        ]
    
    def get_drives_for_backup(self, drives_to_backup: str = 'all') -> List[Drive]:
        if drives_to_backup == 'all':
            return self.drive_list
        else:
            return [self.find_drive_by_name(drives_to_backup)]

    def find_drive_by_name(self, drive_name: str) -> Drive:
        for drive in self.drive_list:
            if drive.drive_name.lower() == drive_name.lower():
                return drive

    def get_backup_directory_path(self, backup_to_local_drive: bool = True) -> Path:
        if backup_to_local_drive:
            return Path(self.data['local_backup_drive']['drive_location'])
        else:
            return Path(self.data['portal_backup_drive']['drive_location'])