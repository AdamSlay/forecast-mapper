FROM ubuntu:latest
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential \
      clang \
      gdb \
      cmake

RUN useradd -u 8877 png-user
COPY --chown=png-user: png-mapper /src/vol
USER png-user

# docker run -it --rm --name=png-mapper \
#--mount type=bind,source=${PWD},target=/src \
#png-mapper-builder \
#bash
