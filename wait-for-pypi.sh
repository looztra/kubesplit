#!/usr/bin/env bash

PACKAGE_VERSION=$1
PACKAGE_NAME=$2
while true; do
  date
  pip install "${PACKAGE_NAME}"=="${PACKAGE_VERSION}" || true
  if hash "${PACKAGE_NAME}"; then
    echo "Found expected version, let's go on"
    break
  else
    echo "Did not find the expected version [${PACKAGE_VERSION}] for package [${PACKAGE_NAME}], sleeping 15s"
    sleep 15s
  fi
done
