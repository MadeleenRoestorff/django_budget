#! /usr/bin/env python3

import re
import os
import tarfile
import datetime
import requests
import traceback
import subprocess
import sqlite3
import io
import zipfile

try:
    print("Starting backup script...")
    script_dir = os.path.dirname(os.path.realpath(__file__))

    os.chdir(script_dir)
    os.chdir("..")

    try:
        os.mkdir("backups")
    except:
        pass

    start_time = datetime.datetime.now()
    start_time_str = start_time.strftime("%Y_%m_%d__%H_%M_%S")

    # set backup file name
    # backup_file_name = "%s_db_data.tar.gz" % start_time_str
    backup_file_name = "%s_db_backup.db" % start_time_str
    dump_file_name = "%s_db_dump.zip" % start_time_str
    backup_path = os.path.join("backups", backup_file_name)
    dump_path = os.path.join("backups", dump_file_name)

    # log status db pages
    def progress(status, remaining, total):
        print(f'Copied {total - remaining} of {total} pages...')

    try:
        # existing DB
        sqliteCon = sqlite3.connect('db.sqlite3')
        # copy into this DB
        backupCon = sqlite3.connect(backup_path)
        # backup data
        with backupCon:
            sqliteCon.backup(backupCon, pages=0, progress=progress)
        # dump data
        # with io.open(dump_path, 'w') as f:
        #     for line in sqliteCon.iterdump():
        #         f.write('%s\n' % line)

        data = '\n'.join(sqliteCon.iterdump())

        # Create a zip file and write add the dump into it as
        # a new file
        zf = zipfile.ZipFile(dump_path,
                             mode='w',
                             compression=zipfile.ZIP_DEFLATED)
        zf.writestr('dump.sql', data)
        zf.close()

        with zipfile.ZipFile("sample.zip", mode="r") as archive:
...         archive.extractall("output_dir/")

        print("backup successful")

    except sqlite3.Error as error:
        print("Error while taking backup: ", error)
    finally:
        if backupCon:
            backupCon.close()
            sqliteCon.close()


except:
    pass
