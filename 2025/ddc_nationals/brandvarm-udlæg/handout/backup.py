#!/usr/bin/python3
# /root/backup.py - Automated backup script for receipts

import os
import shutil
import datetime
import glob

# Backup source and destination
SRC_DIR = "/app/static/receipts"
BACKUP_DIR = "/var/backups/receipts"

def create_backup():
    # Create timestamp for the backup
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"receipts_backup_{timestamp}.tar.gz"

    # Create backup directory if it doesn't exist
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

    # Create backup using shutil (avoiding shell commands)
    backup_path = os.path.join(BACKUP_DIR, backup_name)

    # Create tar archive
    shutil.make_archive(
        os.path.join(BACKUP_DIR, f"receipts_backup_{timestamp}"),
        'gztar',
        SRC_DIR
    )

    # Clean up old backups (keep last 10)
    old_backups = sorted(glob.glob(os.path.join(BACKUP_DIR, "receipts_backup_*.tar.gz")))
    if len(old_backups) > 10:
        for old_backup in old_backups[:-10]:
            os.remove(old_backup)

if __name__ == "__main__":
    create_backup()