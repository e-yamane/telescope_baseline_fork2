FROM python:3.9
USER root

RUN apt-get update
RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
RUN apt-get install -y vim less

ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

ARG UID
ARG GID
ARG UNAME

ENV UID ${UID}
ENV GID ${GID}
ENV UNAME ${UNAME}

RUN groupadd -g ${GID} ${UNAME} ;exit 0
RUN useradd -u ${UID} -g ${GID} -m ${UNAME}

COPY ./setVolumePermission.sh /home/${UNAME}
RUN chmod +x /home/${UNAME}/setVolumePermission.sh

ENTRYPOINT ["sh", "-c", "/home/${UNAME}/setVolumePermission.sh"]

RUN python -m pip install --upgrade pip setuptools
COPY requirements.txt /tmp
WORKDIR /tmp
RUN python -m pip install -r requirements.txt
