FROM python:3.11

USER root
RUN apt-get update && apt-get install -y xvfb sudo curl && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

COPY requirements.txt .
RUN pip install -r requirements.txt

CMD ["/bin/bash"]