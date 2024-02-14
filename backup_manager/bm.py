#!/home/bardia/Desktop/dotin-edu-tasks/dotin-edu-tasks-project01/venv/bin/python
import argparse
import os
import sys
import subprocess
from datetime import datetime, timedelta

# Directory where backup configurations are stored
BACKUP_DIR = "/home/bardia/Desktop/dotin-edu-tasks/dotin-edu-tasks-project01/backup_manager/backups"

def setup_new_backup(crontab_format, src_path, des_path):
  """
  Set up a new backup by writing it to crontab.
  """
  # Validate paths and crontab format (you can add more validation logic)
  if not os.path.exists(src_path) or not os.path.exists(des_path):
    print("Error: Source or destination path does not exist.")
    sys.exit(1)

  # Add the crontab entry for the backup
  crontab_entry = f"{crontab_format} /usr/bin/rsync -a {src_path} {des_path}"
  subprocess.run(["crontab", "-l"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  subprocess.run(["crontab", "-l", "|", "grep", "-v", crontab_entry], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  subprocess.run(["echo", crontab_entry, "|", "crontab", "-"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  print(f"Backup scheduled: {crontab_entry}")

# def list_backups():
#   """
#   Show a list of configured backups.
#   """
#   backups = os.listdir(BACKUP_DIR)
#   print("Configured backups:")
#   for backup in backups:
#     print(f"- {backup}")
  
def list_backups():
    """
    Show a list of configured backups from crontab.
    """
    try:
        crontab_output = subprocess.check_output(["crontab", "-l"], stderr=subprocess.PIPE, text=True)
        print("Configured backups in crontab:")
        print(crontab_output)

    except subprocess.CalledProcessError:
        print("Error: Unable to retrieve crontab entries.")
        sys.exit(1)

def delete_old_backups(time_period, backup_id):
  """
  Delete backups older than the given time period.
  """
  try:
    # Convert time_period (e.g., "7d" for 7 days) to timedelta
    period, unit = int(time_period[:-1]), time_period[-1]
    if unit == "d":
      delta = timedelta(days=period)
    elif unit == "w":
      delta = timedelta(weeks=period)
    else:
      print("Error: Invalid time period. Use 'd' for days or 'w' for weeks.")
      sys.exit(1)

    backup_path = os.path.join(BACKUP_DIR, backup_id)
    for filename in os.listdir(backup_path):
      file_path = os.path.join(backup_path, filename)
      file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
      if datetime.now() - file_mtime > delta:
        os.remove(file_path)
        print(f"Deleted: {file_path}")

  except Exception as e:
    print(f"Error deleting backups: {e}")
    sys.exit(1)

def main():
  parser = argparse.ArgumentParser(description="Backup Manager (bm)")
  parser.add_argument("--schedule", "-s", nargs=3, metavar=("crontab_format", "src_path", "des_path"),
            help="Setup a new backup")
  parser.add_argument("--list", action="store_true", help="Show list of configured backups")
  parser.add_argument("--older-than", nargs=2, metavar=("time_period", "backup_id"),
            help="Delete backups older than given period")
 # parser.add_argument("--help", "-h", action="store_true", help="Show help")

  args = parser.parse_args()

  if args.schedule:
    setup_new_backup(*args.schedule)
  elif args.list:
    list_backups()
  elif args.older_than:
    delete_old_backups(*args.older_than)
  else:
    parser.print_help()

if __name__ == "__main__":
  main()
