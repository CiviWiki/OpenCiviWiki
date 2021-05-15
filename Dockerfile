FROM python:3.7
EXPOSE 8000
ENV PYTHONUNBUFFERED 1
WORKDIR /app


RUN apt-get update && apt-get install -y --no-install-recommends \
  git \
  gcc \
  vim \
  build-essential \
  unzip \
  xvfb \
  libxi6 \
  libgconf-2-4 \
  default-jdk \
  supervisor && \
  apt-get clean && /

RUN wget https://selenium-release.storage.googleapis.com/3.9/selenium-server-standalone-3.9.0.jar && mv selenium-server-standalone-3.9.0.jar /usr/selenium-server-standalone.jar

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