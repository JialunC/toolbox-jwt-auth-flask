FROM python:3.8-slim-buster
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8 
ENV LC_ALL=C.UTF-8
RUN \
    apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y gcc libpq-dev netcat && \
    apt-get -y clean
RUN rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY ./requirements.dev.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY ./app /usr/src/app
WORKDIR /usr/src/app