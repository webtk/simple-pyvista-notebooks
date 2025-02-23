FROM jupyter/base-notebook:python-3.10
USER root
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libx11-xcb1 \
    libxrender1 \
    libxcomposite1 \
    libxtst6 \
    libxrandr2 \
    libxcb1 \
    libx11-6 \
    xvfb \
    && rm -rf /var/lib/apt/lists/*
USER $NB_UID
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
COPY *.ipynb /home/jovyan/
CMD Xvfb :99 -screen 0 1024x768x24 & export DISPLAY=:99 && jupyter lab --ip=0.0.0.0