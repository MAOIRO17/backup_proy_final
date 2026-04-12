cd /mnt/bigdata

git remote set-url origin https://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@github.com/MAOIRO17/backup_proy_final.git
git config --global core.quotepath false
git add .
git commit -m "Backup: $(date '+%Y-%m-%d %H:%M:%S')"
git push origin main
