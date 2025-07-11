# Stage 1 - Compile needed python dependencies
FROM python:3.12-slim-bookworm AS build

RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends \
        pkg-config \
        build-essential \
        libpq-dev \
         # required for (log) routing support in uwsgi
         libpcre3 \
         libpcre3-dev \
        git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Use uv to install dependencies
RUN pip install uv -U
COPY ./requirements.txt /app/requirements.txt
RUN uv pip install --system -r requirements.txt


WORKDIR /app

# copy source code
COPY ./src /app/src

# Stage 3 - Build docker image suitable for execution and deployment
FROM python:3.12-slim-bookworm AS production

# Stage 3.1 - Set up the needed production dependencies
# install all the dependencies for GeoDjango
RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends \
        # bare minimum to debug live containers
        procps \
        nano \
        # serve correct Content-Type headers
        mime-support \
        # (geo) django dependencies
        postgresql-client \
        gettext \
        binutils \
        libpcre3 \
        libproj-dev \
        gdal-bin \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY docker_start.sh /start.sh
COPY wait_for_db.sh /wait_for_db.sh

RUN mkdir /app/log /app/config /app/media /app/private-media /app/tmp

# copy backend build deps
COPY --from=build /usr/local/lib/python3.12 /usr/local/lib/python3.12
COPY --from=build /usr/local/bin/uvicorn /usr/local/bin/uvicorn
# COPY ./config /app/config
COPY ./src /app/src

RUN groupadd -g 1000 openzaak \
    && useradd -M -u 1000 -g 1000 openzaak \
    && chown -R openzaak:openzaak /app

# drop privileges
USER openzaak

ARG COMMIT_HASH
ARG RELEASE
ENV GIT_SHA=${COMMIT_HASH}
ENV RELEASE=${RELEASE}

LABEL org.label-schema.vcs-ref=$COMMIT_HASH \
      org.label-schema.vcs-url="https://github.com/open-zaak/open-zaak" \
      org.label-schema.version=$RELEASE \
      org.label-schema.name="Open Zaak"

EXPOSE 8000
RUN pip install uvicorn
CMD ["/start.sh"]

