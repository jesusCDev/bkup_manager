from pathlib import Path
import logging
import argparse

from drive_manager.drive_manager import DriveManager
from backup_manager.backup_manager import BackupManager
from backup_manager.backup_manager import OutputHandler
from constants import OPTION_ALL, OPTION_LOCAL, OPTION_PORTAL


def parse_arguments(drive_list: list) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Backup program for drives")
    
    parser.add_argument("-l", "--location", choices=[OPTION_LOCAL, OPTION_PORTAL], help="backup location", required=True)
    parser.add_argument("-d", "--drive", choices=[OPTION_ALL] + [drive.backup_folder_name for drive in drive_list], help="which drive to backup", required=True)
    parser.add_argument("-p", "--production", help="Production Run", action='store_true')
    parser.add_argument("-t", "--test", help="Test Run", action='store_true')
    
    return parser.parse_args()

def configure_logging(is_test_mode: bool) -> None:
    log_level = logging.DEBUG if is_test_mode else logging.INFO
    
    logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')
    
def main() -> None:
    OutputHandler.print_header_message()
    
    script_dir        = Path(__file__).resolve().parent
    drive_manager     = DriveManager(script_dir)
    drive_list        = drive_manager.drive_list
    args              = parse_arguments(drive_list)
    is_local_location = args.location == OPTION_LOCAL
    
    configure_logging(args.test)
    logging.debug(f"Arguments: {args}")
    
    backup_manager                   = BackupManager(args.production, script_dir)
    path_to_drive_to_backup_files_to = drive_manager.get_backup_directory_path(is_local_location)
    
    for drive in drive_manager.get_drives_for_backup(args.drive):
        drive.set_backup_data(is_local_location)
        backup_manager.backup_drive(drive, path_to_drive_to_backup_files_to)

if __name__ == "__main__":
    main()
