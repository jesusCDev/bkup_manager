
from colorama import Fore, Style
import subprocess
import os
import logging
import shutil
from pathlib import Path
from backup_manager.backup_metrics_tracker import BackupMetricsTracker
from backup_manager.output_handler import OutputHandler
from drive_manager.drive import Drive


class BackupManager:
    production_run  = False
    metrics_tracker = None
    
    def __init__(self, production_run: bool, script_dir: str) -> None:
        self.production_run  = production_run
        self.metrics_tracker = BackupMetricsTracker(script_dir, production_run)
        self.output_handler  = OutputHandler(production_run)

    def send_backup_complete_notification(self, message: str) -> None:
        if self.production_run:
            notify_cmd = ["notify-desktop", "-i", "down", "-u", "critical", "Backup Complete", message]
            
            subprocess.run(notify_cmd)
    
    def construct_rsync_command(self, main_folder_path: str, backup_folder_path: str, exclude_folder_list: list) -> None:
        RSYNC_CMD    = f"rsync -avhl --delete --progress --ignore-existing "
        EXCLUDE_FLAG = f"--exclude"
        
        self.metrics_tracker.main_path = main_folder_path
    
        for excluded_folder in exclude_folder_list:
            RSYNC_CMD += f'{EXCLUDE_FLAG} "{excluded_folder}" '
            
            self.metrics_tracker.record_excluded_folder(excluded_folder)
        
        return f"{RSYNC_CMD} '{main_folder_path}' '{backup_folder_path}'"
    
    def execute_rsync_command(self, rsync_cmd: str) -> None:
        if self.production_run:
            self.output_handler.print_separator()
            
        self.output_handler.print_rsync_command_info(self.metrics_tracker)
        logging.debug(f"Rsync Command: {rsync_cmd}")
        
        if self.production_run:
            subprocess.run(rsync_cmd, shell=True)
            self.output_handler.print_separator()
    
    @staticmethod
    def create_directory_if_not_exists(folder_path: Path) -> None:
        folder_path.mkdir(parents=True, exist_ok=True)
    
    def backup_directory(self, main_folder_path: str, backup_folder_path: str, exclude_folder_list: list) -> None:
        self.create_directory_if_not_exists(backup_folder_path)
        
        rsync_cmd = self.construct_rsync_command(main_folder_path, backup_folder_path, exclude_folder_list)
        
        self.execute_rsync_command(rsync_cmd)
    
    def delete_untracked_directories(self, backup_folder_path: Path, directories: list) -> None:
        backup_folders = [f.name for f in os.scandir(backup_folder_path) if f.is_dir()]
        
        for folder in backup_folders:
            if folder not in directories:
                folder_path = backup_folder_path / folder
                
                self.metrics_tracker.record_removed_folder(str(folder_path))
                
                if self.production_run:
                    self.output_handler.print_removing_folder(str(folder_path))
                    shutil.rmtree(folder_path)
                    
                    
        self.output_handler.print_removed_item(self.metrics_tracker)
    
    def backup_drive(self, drive: Drive, backup_path: Path) -> None:
        self.metrics_tracker.initialize_backup(drive.drive_name, str(backup_path))
        self.output_handler.print_starting_message(drive, backup_path)

        directories           = drive.directories
        excluded_main_folders = drive.excluded_main_folders
        excluded_sub_folders  = drive.excluded_sub_folders
        backup_folder_path    = Path(backup_path) / drive.backup_folder_name
    
        self.metrics_tracker.start_backup_timer()
        
        # * Remove any untracked folders
        self.delete_untracked_directories(backup_folder_path, directories)
        
        # * Backup Main Folders to Backup Location
        for folder in directories:
            if folder not in excluded_main_folders:
                self.metrics_tracker.record_modified_folders(folder)
                
                sub_folders_to_exclude = excluded_sub_folders.get(folder, [])
                main_folder_path       = Path(drive.drive_location) / folder
                
                self.backup_directory(main_folder_path, backup_folder_path, sub_folders_to_exclude)
                
        # * Complete Methods
        self.metrics_tracker.stop_backup_timer()
        self.output_handler.print_backup_complete_message(self.metrics_tracker)
        self.send_backup_complete_notification(f"{drive.drive_name} Completed")
        self.metrics_tracker.finalize_backup()