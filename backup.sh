cd /mnt/bigdata

USUARIO="MartínOis"
TOKEN="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"
REPO="backup_proy_final"

git remote set-url origin https://${USUARIO}:${TOKEN}@github.com/MAOIRO17/${REPO}.git

git add .
git commit -m "Backup: $(date +'%Y-%m-%d %H:%M:%S')"
git push origin main
