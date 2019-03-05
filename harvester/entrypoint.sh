#!/usr/bin/env bash

# Exit immediately on error
set -e

# The git commit gets stored during the execution of start.bash
# Here we load the stored commit to be able to output it when running commands
export DJANGO_GIT_COMMIT=$(cat ./.commit)

# We're serving static files through Whitenoise
# See: http://whitenoise.evans.io/en/stable/index.html#
# If you doubt this decision then read the "infrequently asked question" section for details
# Here we gather static files that get served through uWSGI if they don't exist
if [ ! -d "statics" ]; then
    ./manage.py collectstatic --noinput
fi

# Executing the normal commands
exec "$@"
