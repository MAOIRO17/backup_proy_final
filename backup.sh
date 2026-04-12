cd /mnt/bigdata
git remote set-url origin https://github.com/MAOIRO17/backup_proy_final.git
git config --global core.quotepath false
git add .
git commit -m "Backup: $(date '+%Y-%m-%d %H:%M:%S')"
git push origin main
