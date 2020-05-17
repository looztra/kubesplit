FROM python:3.8.3-alpine3.11

ARG CI_PLATFORM
LABEL io.nodevops.ci-platform ${CI_PLATFORM}
LABEL org.label-schema.schema-version "1.0"
LABEL org.label-schema.name "kubesplit"
LABEL org.label-schema.description "kubesplit packaged as a docker image"
LABEL org.label-schema.vcs-url "https://github.com/looztra/kubesplit"
LABEL org.label-schema.vendor "looztra"
LABEL org.label-schema.docker.cmd.help "docker run --rm -v $(pwd):/app/code looztra/kubesplit:TAG help"
LABEL org.label-schema.docker.cmd "docker run --rm -v $(pwd):/app/code looztra/kubesplit:TAG -i input"

WORKDIR /app/code
COPY wait-for-pypi.sh /app/code
ENTRYPOINT ["kubesplit"]
CMD ["--help"]
ARG GIT_SHA1
ARG GIT_BRANCH
ARG CI_BUILD_NUMBER
LABEL org.label-schema.version ${KUBESPLIT_VERSION}
LABEL org.label-schema.vcs-ref ${GIT_SHA1}
LABEL io.nodevops.git-branch ${GIT_BRANCH}
LABEL io.nodevops.ci-build-number ${CI_BUILD_NUMBER}

ARG KUBESPLIT_VERSION
RUN chmod +x /app/code/wait-for-pypi.sh \
  && /app/code/wait-for-pypi.sh ${KUBESPLIT_VERSION} kubesplit \
  && pip install --no-cache-dir kubesplit==${KUBESPLIT_VERSION}
