# Dockerfile - blueprint for docker image

# from image:tag
FROM python:3.10

# get the geopandas requirements from apt before installing with pip
RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential \
  libatlas-base-dev \
  libgdal-dev \
  gfortran

# copy source, destination
COPY data-mapper/requirements.txt .

# run command, '--no-cache-dir' to remove install files(*.tar.gz and other such files)
# this helps keep the image small
RUN pip install --no-cache-dir -r requirements.txt && useradd --create-home -u 8887 mapper-user && mkdir -p /src/data-vol

WORKDIR /home/mapper-user

#change permissions of /data so forecast-user has ownership
COPY --chown=mapper-user: data-mapper/data data/
COPY --chown=mapper-user: data-mapper/src/ .

RUN chown mapper-user /src/data-vol

USER mapper-user

# CMD to run when the container is opened
CMD ["python3", "src/mapper.py"]
