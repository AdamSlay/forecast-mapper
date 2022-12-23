FROM ubuntu:jammy
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential \
      clang \
      gdb \
      cmake \
      netcat
#      git \
#      golang

RUN mkdir -p /src/vol /base/images && useradd -u 8887 png-user && chown png-user /src /src/vol /base/images
COPY --chown=png-user: png-mapper/ /src
USER png-user
