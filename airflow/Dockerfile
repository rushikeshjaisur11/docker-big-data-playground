FROM apache/airflow:2.5.2

USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential libopenmpi-dev \
    && apt-get install libsasl2-dev \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt