#################################################
# BUILD
#################################################

FROM node:12.13 AS builder

RUN mkdir -p /usr/src/rateapp
WORKDIR /usr/src/rateapp

# Adding an app user to prevent container access as root
# Most options speak for itself.
# The -r options make it a system user and group.
# The -m option forces a home folder (which Python/JS tools rely upon rather heavily)
RUN groupadd -r app -g 1001 && useradd app -u 1001 -r -m -g app
# Give access to app user
RUN chown app:app /usr/src/rateapp
# Become app user to prevent attacks during install (possibly from hijacked npm packages)
USER app:app

COPY --chown=app rateapp /usr/src/rateapp

RUN npm install && npm run build


#################################################
# SERVICE
#################################################

FROM python:3.6-stretch

RUN apt-get update && apt-get install -y less vim ffmpeg \
    time dialog sox subversion build-essential zlib1g-dev automake autoconf libtool libatlas3-base

# Create the app environment
RUN mkdir -p /usr/src/app
RUN mkdir -p /usr/src/rateapp
RUN mkdir -p /usr/src/logs
RUN mkdir -p /usr/src/media
WORKDIR /usr/src/app

# Adding an app user to prevent container access as root
# Most options speak for itself.
# The -r options make it a system user and group.
# The -m option forces a home folder (which Python tools rely upon rather heavily)
# We also add default Python user path to PATH so installed binaries get found
RUN groupadd -r app -g 1001 && useradd app -u 1001 -r -m -g app
ENV PATH="/home/app/.local/bin:${PATH}"
# Give access to app user
RUN chown app:app /usr/src/app
RUN chown app:app /usr/src/rateapp
RUN chown app:app /usr/src/logs
RUN chown app:app /usr/src/media
# Become app user to prevent attacks during install (possibly from hijacked PyPi packages)
USER app:app

# Python dependencies
COPY harvester/requirements.txt /usr/src/app/
RUN pip install -U --no-cache-dir --user pip && pip install --no-cache-dir --user uwsgi==2.0.18
RUN pip install --no-cache-dir --user -r requirements.txt

# Copy application
COPY harvester /usr/src/app
COPY --from=builder /usr/src/rateapp/dist /usr/src/rateapp/dist

# Entrypoint sets our environment correctly
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

# The default command is to start a uWSGI server
CMD ["uwsgi", "--ini", "/usr/src/app/uwsgi.ini"]

# EXPOSE port 8000 to allow communication to/from server
EXPOSE 8000
