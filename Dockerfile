# The dockerfile uses multi-stage builds to build the application
# and then copy the build artifacts to the final image. This helps for the layer optimization.
# https://docs.docker.com/develop/develop-images/multistage-build/
#
# Environment replacement
#   - "PYTHONDONTWRITEBYTECODE 1": Python won’t try to write .pyc files on the import of source modules
#     It make sense in a container, since the process runs just once.
#   
#   - "PYTHONUNBUFFERED 1": Force the stdout and stderr streams to be unbuffered. This option has no effect on the stdin stream.
#   - "PIP_NO_CACHE_DIR 1": Disable pip cache, used to shrink the image size by disabling the cache.
#   
#   - PATH: defining virtual enviroment in /opt, since is used to reserved for the installation of add-on application software packages.
#     This can help with with minimizing docker image size when doing multi-staged builds.
#   
# WORKDIR: https://docs.docker.com/engine/reference/builder/
#   - WORKDIR /app: set the working directory for any RUN, CMD, ENTRYPOINT, COPY and ADD instructions that follow it in the Dockerfile.
#   - we don't even need to run mkdir /app since WORKDIR will make it for us.
#   - good practice because we can set a directory as the main directory
# "COPY . .": the contents of the build context directory will be copied to the /myapp dir inside your docker image.
# (COPY <src: "relative to the build context directory"> (TO) <dest: "relative to the WORKDIR directory">)

### build stage ###
FROM python:3.9 AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_NO_CACHE_DIR 1
ENV PATH="/opt/venv/bin:$PATH"

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    python -m venv /opt/venv

COPY requirements.txt .
RUN pip install -r requirements.txt

### final stage ###
FROM python:3.9-slim

WORKDIR /app

ENV PATH="/opt/venv/bin:$PATH"

COPY --from=builder /opt/venv /opt/venv
COPY . .