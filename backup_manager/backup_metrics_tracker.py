from datetime import datetime
import json

from constants import OPTION_LOCAL, OPTION_PORTAL


class BackupMetricsTracker:
    # * Backup Info
    drive_name         = ''
    backup_folder_path = ''
    backup_type        = ''
    production_run     = False
    
    # * JSON Data
    backup_data       = None
    metrics_file_path = None
    
    # * Run Per Drive Info
    run_date        = None
    start_time      = None
    end_time        = None
    length_of_run   = None
    
    # * Drive Info
    folders_updated = []
    removed_folders = []
    
    # * Individual Folder Data
    main_folder      = ''
    excluded_folders = []
      
    def __init__(self, script_dir: str, production_run: bool):
        self.production_run    = production_run
        self.backup_type       = OPTION_PORTAL if production_run else OPTION_LOCAL
        self.metrics_file_path = script_dir / 'logs/backup_manager.json'

        with self.metrics_file_path.open() as drives_file:
            self.backup_data = json.load(drives_file)
        
    def initialize_backup(self, drive_name: str, backup_folder_path: str) -> None:
        self.drive_name         = drive_name
        self.backup_folder_path = backup_folder_path
        self.run_date           = datetime.now().strftime("%Y - %m-%d | %I:%M %p")

    def finalize_backup(self) -> None:
        # * Save Data to JSON
        if self.production_run:
            drive_data      = {
                'drive_name'     : self.drive_name,
                'backup_path'    : self.backup_folder_path,
                'remove_folder'  : self.removed_folders,
                'run_date'       : self.run_date,
                'start_time'     : self.start_time.strftime("%I:%M %p"),
                'end_time'       : self.end_time.strftime("%I:%M %p"),
                'length_of_run'  : str(self.length_of_run),
                'folders_updated': self.folders_updated
            }
            
            backup_data     = self.backup_data.setdefault(self.backup_type, {})
            drive_data_list = backup_data.setdefault(self.drive_name, [])
            
            drive_data_list.append(drive_data)
        
            with self.metrics_file_path.open('w') as drives_file:
                json.dump(self.backup_data, drives_file)
        
        #  * reset folder specific backup_data
        self.removed_folders = []
        self.folders_updated = []
        
    def record_modified_folders(self, main_folder: str) -> None:
        # * - Dump Folder Data to List
        if len(self.main_folder) > 0:
            self.folders_updated.append({
                'main_folder'     : self.main_folder,
                'excluded_folders': self.excluded_folders
            })
        
        # * - Reset Folder Data to None
        self.main_folder      = main_folder
        self.excluded_folders = []
        
    def record_removed_folder(self, folder_path: str) -> None:
        self.removed_folders.append(folder_path)
        
    def record_excluded_folder(self, folder_path: str) -> None:
        self.excluded_folders.append(folder_path)
        
    def start_backup_timer(self) -> None:
        self.start_time = datetime.now()
        
    def stop_backup_timer(self) -> None:
        self.end_time      = datetime.now()
        self.length_of_run = self.end_time - self.start_time

    def get_backup_duration(self) -> str:
        if self.length_of_run is not None:
            hours  , remainder = divmod(self.length_of_run.total_seconds(), 3600)
            minutes, seconds   = divmod(remainder, 60)
            
            # return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
            return "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))
        else:
            return 'N/A'