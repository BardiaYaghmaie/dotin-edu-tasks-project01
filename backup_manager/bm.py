import argparse
import os
import subprocess
import sys
import shutil
from datetime import datetime, timedelta

# Constants
CONFIG_FILE = "backups.cfg"
BACKUPS_DIR = "backups"

def setup_backup(crontab_format, src_path, des_path):
    """
    Setup a new backup with the given crontab format, source path, and destination path.
    """
    # Create backups directory if it doesn't exist
    os.makedirs(BACKUPS_DIR, exist_ok=True)
    
    # Create unique backup id based on current timestamp
    backup_id = datetime.now().strftime("%Y%m%d%H%M%S")
    
    # Write backup configuration to file
    with open(CONFIG_FILE, "a") as f:
        f.write(f"{backup_id},{crontab_format},{src_path},{des_path}\n")
    
    print(f"Backup scheduled successfully with ID: {backup_id}")

def list_backups():
    """
    Show list of configured backups.
    """
    if not os.path.exists(CONFIG_FILE):
        print("No backups configured yet.")
        return
    
    with open(CONFIG_FILE, "r") as f:
        backups = [line.strip().split(",") for line in f.readlines()]
    
    print("Configured Backups:")
    for backup in backups:
        print(f"ID: {backup[0]}, Schedule: {backup[1]}, Source: {backup[2]}, Destination: {backup[3]}")

def delete_old_backups(time_period, backup_id):
    """
    Delete backups older than the given time period for the specified backup ID.
    """
    backups_to_delete = []
    current_time = datetime.now()
    
    with open(CONFIG_FILE, "r") as f:
        backups = [line.strip().split(",") for line in f.readlines()]
    
    for backup in backups:
        if backup[0] == backup_id:
            src_path = os.path.join(BACKUPS_DIR, backup[0])
            if os.path.exists(src_path):
                backup_time = datetime.strptime(backup[0], "%Y%m%d%H%M%S")
                if current_time - backup_time > timedelta(days=time_period):
                    backups_to_delete.append(src_path)
    
    for backup_path in backups_to_delete:
        try:
            shutil.rmtree(backup_path)
            print(f"Backup {backup_path} deleted successfully.")
        except Exception as e:
            print(f"Error deleting backup {backup_path}: {e}")

def parse_args():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(description="Backup Manager")
    subparsers = parser.add_subparsers(dest="command")
    
    # Subparser for setting up a new backup
    parser_setup = subparsers.add_parser("setup", help="Setup a new backup")
    parser_setup.add_argument("--schedule", "-s", required=True, help="Crontab format for scheduling the backup")
    parser_setup.add_argument("src_path", help="Source path")
    parser_setup.add_argument("des_path", help="Destination path")
    
    # Subparser for listing configured backups
    subparsers.add_parser("list", help="Show list of configured backups")
    
    # Subparser for performing housekeeping
    parser_housekeeping = subparsers.add_parser("housekeeping", help="Delete old backups")
    parser_housekeeping.add_argument("--older-than", required=True, type=int, help="Time period in days")
    parser_housekeeping.add_argument("backup_id", help="Backup ID")
    
        
    return parser.parse_args()

def main():
    args = parse_args()
    
    if args.command == "setup":
        setup_backup(args.schedule, args.src_path, args.des_path)
    elif args.command == "list":
        list_backups()
    elif args.command == "housekeeping":
        delete_old_backups(args.older_than, args.backup_id)

if __name__ == "__main__":
    main()
