#!/bin/bash

sleep 30

backup_dir="/home/suporte/Documentos/backups_setorT"

backup_file="$backup_dir/backup_$(date +"%Y%m%d%H%M%S").sql"

pg_dump_command="pg_dump -U usuario_postgres -d nome_banco_dados -f $backup_file -h db"

$pg_dump_command
