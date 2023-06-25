FROM python:3.11-slim-bullseye

LABEL org.label-schema.schema-version "1.0" \
  org.label-schema.name "kubesplit" \
  org.label-schema.description "kubesplit packaged as a docker image" \
  org.label-schema.vcs-url "https://github.com/looztra/kubesplit" \
  org.label-schema.vendor "looztra" \
  org.label-schema.docker.cmd.help "docker run --rm -v $(pwd):/app/code looztra/kubesplit:TAG help" \
  org.label-schema.docker.cmd "docker run --rm -v $(pwd):/app/code looztra/kubesplit:TAG -i input"
ENV PIP_ROOT_USER_ACTION=ignore

WORKDIR /app/code
COPY wait-for-pypi.sh /app/code
ENTRYPOINT ["kubesplit"]
CMD ["--help"]
ARG GIT_SHA1
ARG GIT_REF
ARG APP_VERSION
LABEL org.label-schema.version ${APP_VERSION} \
  org.label-schema.vcs-ref ${GIT_SHA1} \
  io.nodevops.git-ref=${GIT_REF}

RUN chmod +x /app/code/wait-for-pypi.sh \
  && /app/code/wait-for-pypi.sh ${APP_VERSION} kubesplit \
  && pip install --no-cache-dir kubesplit==${APP_VERSION}
