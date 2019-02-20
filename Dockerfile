FROM python:2.7
EXPOSE 8000
ENV PYTHONUNBUFFERED 1
WORKDIR /app


RUN apt-get update && apt-get install -y --no-install-recommends \
  git \
  gcc \
  vim \
  build-essential \
  supervisor && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade \
    pip \
    wheel \
    --trusted-host pypi.python.org

COPY requirements.txt entrypoint.sh /app/
RUN pip install -r requirements.txt

ADD project /app/
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT [ "/app/entrypoint.sh" ]
CMD [ "localserver" ]