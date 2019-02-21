FROM python:2.7
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
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add && echo "deb [arch=amd64]  http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list

RUN apt-get -y update && apt-get install -y --no-install-recommends google-chrome-stable && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

RUN wget https://chromedriver.storage.googleapis.com/2.46/chromedriver_linux64.zip && unzip chromedriver_linux64.zip && rm chromedriver_linux64.zip
RUN mv chromedriver /usr/bin/chromedriver && chown root:root /usr/bin/chromedriver && chmod +x /usr/bin/chromedriver
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