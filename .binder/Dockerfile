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
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
RUN Xvfb :99 -screen 0 1024x768x24 & export DISPLAY=:99

USER $NB_UID

#ENTRYPOINT ["jupyter", "notebook"]
#CMD ["--ip=0.0.0.0", "--port=8888", "--NotebookApp.token=''"]
#CMD Xvfb :99 -screen 0 1024x768x24 & export DISPLAY=:99 && jupyter lab --ip=0.0.0.0 --allow-root
CMD Xvfb :99 -screen 0 1024x768x24 & export DISPLAY=:99 && jupyter lab --ip=0.0.0.0