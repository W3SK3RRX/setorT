#!/bin/bash

# Diretório onde os backups serão armazenados
BACKUP_DIR="/home/suporte/Documentos/setorT/backups"

# Nome do arquivo de backup (inclui a data atual)
BACKUP_FILE="backup_$(date +%Y-%m-%d_%H-%M-%S).sql"

# Executa o backup usando pg_dump
docker exec -t db pg_dump -U setorT setorT > "$BACKUP_DIR/$BACKUP_FILE"

# OPCIONAL: Compacta o backup (descomente a linha abaixo se desejar)
# gzip "$BACKUP_DIR/$BACKUP_FILE"
