#!/usr/bin/env ash
# shellcheck shell=dash

PACKAGE_VERSION=$1
PACKAGE_NAME=$2
while true; do
    date
    pip install "${PACKAGE_NAME}"=="${PACKAGE_VERSION}" || true
    if hash "${PACKAGE_NAME}"; then
        break
    else
        echo "Did not find the expected version [${PACKAGE_VERSION}] for package [${PACKAGE_NAME}], sleeping"
        sleep 15s
    fi
done
