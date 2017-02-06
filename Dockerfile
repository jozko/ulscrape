FROM python:3.5-alpine

MAINTAINER "Jozko Skrablin"

ENV USER="scrapy"

RUN apk add --no-cache -qq libffi gcc postgresql-dev musl-dev bash libffi-dev libffi-dev libxslt-dev zlib libjpeg-turbo-dev

RUN adduser -D -u 501 ${USER}

RUN mkdir -p /home/${USER}/tmp && \
  mkdir -p /home/$USER/data

ADD . /home/${USER}

RUN chown -R ${USER}:${USER} /home/${USER}

RUN pip --no-cache-dir install dumb-init && \
  pip --no-cache-dir install --upgrade -r /home/${USER}/requirements.txt

WORKDIR /home/${USER}/Code

VOLUME ["/home/${USER}/Code"]

RUN chown -R ${USER}:${USER} /home/${USER}

USER ${USER}

ENTRYPOINT ["/bin/bash"]
