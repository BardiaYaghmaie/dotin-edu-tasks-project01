import argparse
import os
import shutil
from datetime import datetime, timedelta

BACKUPS_DIR = "/path/to/backups"  # Replace with your desired backup directory

def create_backup(src_path, des_path, schedule):
  """
  Creates a backup of the source path to the destination path.

  Args:
    src_path: The path to the source directory to backup.
    des_path: The path to the destination directory for the backup.
    schedule: The crontab-formatted schedule for future backups.
  """
  # Create destination directory if it doesn't exist
  os.makedirs(des_path, exist_ok=True)

  # Generate unique timestamp for backup filename
  timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
  backup_filename = f"{des_path}/{timestamp}.tar.gz"

  # Create the backup archive
  command = f"tar -czvf {backup_filename} {src_path}"
  os.system(command)

  print(f"Backup created: {backup_filename}")

  # Add schedule to file (implement your preferred scheduling mechanism)
  # ...

def list_backups():
  """
  Lists all configured backups.
  """
  entries = [f for f in os.listdir(BACKUPS_DIR) if os.path.isdir(os.path.join(BACKUPS_DIR, f))]
  print("Configured backups:")
  for entry in entries:
    print(f" - {entry}")

def delete_old_backups(backup_id, time_period):
  """
  Deletes backups older than the specified time period for a given backup id.

  Args:
    backup_id: The ID of the backup to clean up (directory name within BACKUPS_DIR).
    time_period: The time period in days to keep backups.
  """
  backup_path = os.path.join(BACKUPS_DIR, backup_id)
  if not os.path.exists(backup_path):
    print(f"Backup ID '{backup_id}' not found.")
    return

  threshold = datetime.now() - timedelta(days=int(time_period))
  for filename in os.listdir(backup_path):
    if filename.endswith(".tar.gz"):
      filepath = os.path.join(backup_path, filename)
      file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
      if file_time < threshold:
        print(f"Deleting old backup: {filepath}")
        os.remove(filepath)

def main():
  parser = argparse.ArgumentParser(description="Backup Manager")
  subparsers = parser.add_subparsers(dest="command")

  # Create backup
  parser_create = subparsers.add_parser("create", aliases=["--schedule", "-s"])
  parser_create.add_argument("src_path", help="The path to the source directory to backup")
  parser_create.add_argument("des_path", help="The path to the destination directory for the backup")
  parser_create.add_argument("schedule", help="The crontab-formatted schedule for future backups")

  # List backups
  parser_list = subparsers.add_parser("list", aliases=["--list"])

  # Delete old backups
  parser_delete = subparsers.add_parser("delete", aliases=["--older-than", "--housekeeping"])
  parser_delete.add_argument("backup_id", help="The ID of the backup to clean up (directory name)")
  parser_delete.add_argument("time_period", help="The time period in days to keep backups")

  # Help
  parser.add_argument("-h", "--help", action="help", help="Show this help message and exit")

  args = parser.parse_args()

  if args.command == "create":
    create_backup(args.src_path, args.des_path, args.schedule)
  elif args.command == "list":
    list_backups()
  elif args.command == "delete":
    delete_old_backups(args.backup_id, args.time_period)
  else:
    parser.print_help()

if __name__ == "__main__":
  main()
