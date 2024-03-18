from pathlib import Path
from typing import List, Dict


class Drive:
    directories           = []
    excluded_main_folders = []
    excluded_sub_folders  = []
    
    def __init__(self, drive_name: str, drive_location: str, backup_folder_name: str, backup_type: str,
                 portal_folder_ignore_list: list, local_folder_ignore_list: list):
        self.drive_name                = drive_name
        self.drive_location            = drive_location
        self.backup_folder_name        = backup_folder_name
        self.backup_type               = backup_type
        self.portal_folder_ignore_list = portal_folder_ignore_list
        self.local_folder_ignore_list  = local_folder_ignore_list
        self.directories               = self.get_directory_names(self.drive_location)
        
    def set_backup_data(self, backup_to_local_drive: bool = True):
        exclude_folder_list        = self.local_folder_ignore_list if backup_to_local_drive else self.portal_folder_ignore_list
        self.excluded_main_folders = self.get_excluded_top_level_directories(exclude_folder_list)
        self.excluded_sub_folders  = self.get_excluded_subdirectories(exclude_folder_list)

    @staticmethod
    def get_directory_names(path: str) -> List[str]:
        return [name.name for name in Path(path).iterdir() if name.is_dir() and not name.name.startswith('.') and name.name != 'lost+found']
    
    @staticmethod
    def get_excluded_top_level_directories(folder_list: List[str]) -> List[str]:
        return [folder for folder in folder_list if '/' not in folder]

    @staticmethod
    def get_excluded_subdirectories(folder_list: List[str]) -> Dict[str, List[str]]:
        excluded_sub_folders = {}

        for folder in folder_list:
            split_folder = folder.split('/')
            
            if len(split_folder) > 1:
                main_folder = split_folder[0]
                sub_folder  = '/'.join(split_folder[1:])
                
                if main_folder in excluded_sub_folders:
                    excluded_sub_folders[main_folder].append(sub_folder)
                else:
                    excluded_sub_folders[main_folder] = [sub_folder]

        return excluded_sub_folders