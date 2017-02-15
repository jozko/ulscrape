FROM python:3.5-alpine

MAINTAINER "Jozko Skrablin"

ENV USER="scrapy"

RUN apk add --no-cache -qq ca-certificates gcc libffi \
  musl-dev bash libffi-dev libffi-dev openssl-dev readline-dev \
  libxslt-dev zlib libjpeg-turbo-dev

RUN adduser -D -u 501 ${USER}

RUN mkdir -p /home/${USER}/tmp && \
  mkdir -p /home/$USER/data

ADD . /home/${USER}

RUN chown -R ${USER}:${USER} /home/${USER}

RUN pip install --disable-pip-version-check --no-cache-dir dumb-init && \
  pip install --disable-pip-version-check --no-cache-dir \
  -r /home/${USER}/requirements.txt

WORKDIR /home/${USER}/Code

VOLUME ["/home/${USER}/Code"]

RUN chown -R ${USER}:${USER} /home/${USER}

USER ${USER}

ENTRYPOINT ["/bin/bash"]
