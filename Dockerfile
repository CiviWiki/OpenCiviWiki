FROM python:3.7
EXPOSE 8000
ENV PYTHONUNBUFFERED 1
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential \
  apt-get clean

# Install Pillow dependencies
RUN apt-get install -y --no-install-recommends \
  ibtiff5-dev \
  libjpeg8-dev \
  libopenjp2-7-dev \
  zlib1g-dev \
  libfreetype6-dev \
  liblcms2-dev \
  libwebp-dev \
  tcl8.6-dev \
  tk8.6-dev \
  python3-tk \
  libharfbuzz-dev \
  libfribidi-dev \
  libxcb1-dev

# Upgrade pip and friends
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
