#!/bin/bash

# 1. Cargar el entorno de Python (Conda)
export PATH="/mnt/bigdata/miniconda/bin:$PATH"
source /mnt/bigdata/miniconda/etc/profile.d/conda.sh
conda activate scraping

# 2. Ir a la carpeta del proyecto
cd /mnt/bigdata

# 3. Subir los cambios a GitHub
git config --global core.quotepath false
git add .
git commit -m "Backup automático: $(date '+%Y-%m-%d %H:%M:%S')"
git push origin main
