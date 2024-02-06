## Step 1
A simple API that echos everything you send to it! Also, write the sent message on a file in the /var/lib/echo_api/{message}

Example:
  Suppose the API is up at your localhost and on port 8080

Request:
  curl -X POST localhost:8080/echo/hi
Response:
  hi

Also, a file will be created at /var/lib/echo_api/hi.

## Step 2
Write a service file for this API. Whenever the computer reboots, this service should be started automatically.

## Step 3
Write a script that works as a backup manager.

Commands:
  bm --schedule|-s {crontab_format} {src_path} {des_path} (Setup a new backup)
  bm --list (Show list of configured backups)
  bm --older-than {time_period} --housekeeping {backup_id} (Delete backups older than given period)
  bm --help|-h (show help)

## Step 4
Set up a backup for your API with your script!
Backup from your API data every 12:30 on even days.
