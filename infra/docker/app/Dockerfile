# ベースとなるビルド
FROM python:3.12-slim-bullseye as base

WORKDIR /opt/python-be-syokyu-app

RUN apt-get update && \
    apt-get -y install gcc libmariadb-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements/*.txt /tmp/python-be-syokyu-tmp/requirements/

RUN python -m pip install --upgrade pip

# dev環境用ステージ
FROM base as dev
RUN pip install -r /tmp/python-be-syokyu-tmp/requirements/dev.txt
CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "18008"]
