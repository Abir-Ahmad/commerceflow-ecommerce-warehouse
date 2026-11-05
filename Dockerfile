FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1 \
    DBT_SEND_ANONYMOUS_USAGE_STATS=false
WORKDIR /app
COPY requirements.lock.txt ./
RUN pip install --no-cache-dir -r requirements.lock.txt
COPY dbt_project.yml ./
COPY profiles/ profiles/
COPY macros/ macros/
COPY models/ models/
COPY tests/ tests/
COPY analyses/ analyses/
COPY scripts/ scripts/
CMD ["python", "scripts/container_smoke.py"]
