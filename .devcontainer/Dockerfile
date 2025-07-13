FROM condaforge/miniforge3:25.3.0-3

COPY environment.yml /tmp/environment.yml
RUN conda env create -f /tmp/environment.yml
# 기본 환경 활성화
SHELL ["bash", "-lc"]

WORKDIR /app
# 진입 스크립트
ENTRYPOINT ["bash", "-lc", "conda activate myenv && python main.py"]