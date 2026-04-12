if [ ! -d "/mnt/bigdata/miniconda" ]; then
    echo "Instalando Miniconda en /mnt/bigdata..."
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
    bash miniconda.sh -b -p /mnt/bigdata/miniconda
    rm miniconda.sh
fi

source /mnt/bigdata/miniconda/bin/activate

if [ ! -d "/mnt/bigdata/miniconda/envs/scraping" ]; then
    echo "Creando entorno 'scraping' e instalando pandas y thefuzz..."
    conda create -n scraping python=3.10 -y
    conda activate scraping
    pip install pandas thefuzz python-Levenshtein notebook
fi
