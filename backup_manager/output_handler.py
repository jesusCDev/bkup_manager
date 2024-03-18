from colorama import Fore, Style
from backup_manager.backup_metrics_tracker import BackupMetricsTracker
from drive_manager.drive import Drive
from pathlib import Path
import textwrap


class OutputHandler:
    LEFT_SPACE_WIDTH = 8
    
    def __init__(self, production_run):
        self.production_run = production_run
        
    def print_removed_item(self, metrics_tracker: BackupMetricsTracker) -> None:
        print(f"{' ' * self.LEFT_SPACE_WIDTH}{Fore.RED}Removed Folders: {Style.RESET_ALL}\n{'\n'.join(' ' * (self.LEFT_SPACE_WIDTH + 4) + folder for folder in metrics_tracker.removed_folders)}")
        
    def print_removing_folder(self, folder: str) -> None:
        print(f"{' ' * self.LEFT_SPACE_WIDTH}{Fore.RED}Removing: {Style.RESET_ALL}{folder}")
    
    def print_rsync_command_info(self, metrics_tracker: BackupMetricsTracker) -> None:
        print(f"\n{" " * self.LEFT_SPACE_WIDTH}{Fore.LIGHTCYAN_EX}Main Path:{Style.RESET_ALL}        {metrics_tracker.main_path}")
        print(f"{' ' * self.LEFT_SPACE_WIDTH}{Fore.YELLOW}Excluded Folders: {Style.RESET_ALL}\n{'\n'.join(' ' * (self.LEFT_SPACE_WIDTH + 4) + folder for folder in metrics_tracker.excluded_folders)}")
        
    def print_starting_message(self, drive: Drive, backup_path: Path) -> None:
        run_type_color = Fore.RED if self.production_run else Fore.WHITE

        print(f'''
        {Fore.LIGHTBLACK_EX}Run Type:         {run_type_color}{"Production" if self.production_run else "Dry"}
        {Fore.LIGHTBLACK_EX}Backing up drive: {Fore.LIGHTCYAN_EX}{drive.drive_name}
        {Fore.LIGHTBLACK_EX}To location:      {Fore.LIGHTCYAN_EX}{backup_path}{Style.RESET_ALL}
        ''')

    @staticmethod
    def print_separator() -> None:
        print(f"\n{'*' * 100}\n")
            
    def print_backup_complete_message(self, metrics_tracker) -> None:
        total_width             = 77
        backup_complete_message = f"🚀 Backup Complete 🚀"
        time_taken_message      = f"Backup took {Fore.WHITE}{metrics_tracker.get_backup_duration()}{Fore.LIGHTMAGENTA_EX} to complete."

        # * Calculate the number of spaces needed on each side for the messages
        spaces_on_each_side_backup = ((total_width - 3) - len(backup_complete_message)) // 2
        spaces_on_each_side_time   = ((total_width - 2) - len("Backup took " + metrics_tracker.get_backup_duration() + " to complete.")) // 2

        print(f'\n\n{Fore.LIGHTMAGENTA_EX}{" " * self.LEFT_SPACE_WIDTH}{"=" * total_width}{Style.RESET_ALL}')
        print(f'{Fore.LIGHTMAGENTA_EX}{" " * self.LEFT_SPACE_WIDTH}|{" " * (total_width - 2)}|{Style.RESET_ALL}')
        print(f'{Fore.LIGHTMAGENTA_EX}{" " * self.LEFT_SPACE_WIDTH}|{" " * spaces_on_each_side_backup}{backup_complete_message}{" " * spaces_on_each_side_backup}|{Style.RESET_ALL}')
        print(f'{Fore.LIGHTMAGENTA_EX}{" " * self.LEFT_SPACE_WIDTH}|{" " * spaces_on_each_side_time}{time_taken_message}{" " * spaces_on_each_side_time}|{Style.RESET_ALL}')
        print(f'{Fore.LIGHTMAGENTA_EX}{" " * self.LEFT_SPACE_WIDTH}|{" " * (total_width - 2)}|{Style.RESET_ALL}')
        print(f'{Fore.LIGHTMAGENTA_EX}{" " * self.LEFT_SPACE_WIDTH}{"=" * total_width}{Style.RESET_ALL}\n\n')

    @staticmethod
    def print_header_message() -> None:
        message = f'''
        {Fore.LIGHTMAGENTA_EX}
        ██████╗  █████╗  ██████╗██╗  ██╗██╗   ██╗██████╗     ███╗   ███╗ █████╗ ███╗   ██╗ █████╗  ██████╗ ███████╗██████╗ 
        ██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██║   ██║██╔══██╗    ████╗ ████║██╔══██╗████╗  ██║██╔══██╗██╔════╝ ██╔════╝██╔══██╗
        ██████╔╝███████║██║     █████╔╝ ██║   ██║██████╔╝    ██╔████╔██║███████║██╔██╗ ██║███████║██║  ███╗█████╗  ██████╔╝
        ██╔══██╗██╔══██║██║     ██╔═██╗ ██║   ██║██╔═══╝     ██║╚██╔╝██║██╔══██║██║╚██╗██║██╔══██║██║   ██║██╔══╝  ██╔══██╗
        ██████╔╝██║  ██║╚██████╗██║  ██╗╚██████╔╝██║         ██║ ╚═╝ ██║██║  ██║██║ ╚████║██║  ██║╚██████╔╝███████╗██║  ██║
        ╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝         ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
        {Style.RESET_ALL}
        {Fore.YELLOW}
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        {Style.RESET_ALL}
        '''
    
        print(message)