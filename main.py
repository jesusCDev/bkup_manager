from pathlib import Path
import logging
import argparse

from drive_manager.drive_manager import DriveManager
from backup_manager.backup_manager import BackupManager
from backup_manager.backup_manager import OutputHandler


def main():
    OPTION_LOCAL  = 'local'
    OPTION_PORTAL = 'portal'
    OPTION_ALL    = 'all'

    OutputHandler.print_header_message()
    
    script_dir    = Path(__file__).resolve().parent
    drive_manager = DriveManager(script_dir)
    drive_list    = drive_manager.drive_list
    
    parser = argparse.ArgumentParser(description="Backup program for drives")
    
    parser.add_argument("-l", "--location", choices=[OPTION_LOCAL, OPTION_PORTAL], help="backup location", required=True)
    parser.add_argument("-d", "--drive", choices=[OPTION_ALL] + [drive.backup_folder_name for drive in drive_list], help="which drive to backup", required=True)
    parser.add_argument("-p", "--production", help="Production Run", action='store_true')
    parser.add_argument("-t", "--test", help="Test Run", action='store_true')
    
    args                  = parser.parse_args()
    drives_to_backup      = args.drive
    backup_to_local_drive = True if args.location == OPTION_LOCAL else False
    log_level             = logging.DEBUG if args.test else logging.INFO
    
    logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.debug(f"Arguments: {args}")

    backup_manager                   = BackupManager(args.production, script_dir)
    path_to_drive_to_backup_files_to = drive_manager.get_backup_directory_path(backup_to_local_drive)
    
    
    for drive in drive_manager.get_drives_for_backup(drives_to_backup):
        drive.set_backup_data(backup_to_local_drive)
        backup_manager.backup_drive(drive, path_to_drive_to_backup_files_to)

if __name__ == "__main__":
    main()
