source /mnt/bigdata/miniconda/etc/profile.d/conda.sh
conda activate scraping

cd /mnt/bigdata
git config --global core.quotepath false
git add .
git commit -m "Backup: $(date '+%Y-%m-%d %H:%M:%S')"
git push origin main
