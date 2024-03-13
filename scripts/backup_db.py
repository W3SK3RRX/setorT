import subprocess
import os
import datetime


backup_dir = "/home/suporte/Documentos/backups_setorT"

backup_file = os.path.join(backup_dir, f"backup_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.sql")

pg_dump_command = f"pg_dump -U setorT -d setorT -f {backup_file}"

subprocess.run(pg_dump_command, shell=True)