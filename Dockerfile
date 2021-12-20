FROM python:3.9-slim-buster

ARG CI_PLATFORM
LABEL io.nodevops.ci-platform ${CI_PLATFORM} \
	org.label-schema.schema-version "1.0" \
	org.label-schema.name "kubesplit" \
	org.label-schema.description "kubesplit packaged as a docker image" \
	org.label-schema.vcs-url "https://github.com/looztra/kubesplit" \
	org.label-schema.vendor "looztra" \
	org.label-schema.docker.cmd.help "docker run --rm -v $(pwd):/app/code looztra/kubesplit:TAG help" \
	org.label-schema.docker.cmd "docker run --rm -v $(pwd):/app/code looztra/kubesplit:TAG -i input"

WORKDIR /app/code
COPY wait-for-pypi.sh /app/code
ENTRYPOINT ["kubesplit"]
CMD ["--help"]
ARG GIT_SHA1
ARG GIT_BRANCH
ARG CI_BUILD_NUMBER
LABEL org.label-schema.version ${KUBESPLIT_VERSION} \
	org.label-schema.vcs-ref ${GIT_SHA1} \
	io.nodevops.git-branch ${GIT_BRANCH} \
	io.nodevops.ci-build-number ${CI_BUILD_NUMBER}

ARG KUBESPLIT_VERSION
RUN chmod +x /app/code/wait-for-pypi.sh \
	&& /app/code/wait-for-pypi.sh ${KUBESPLIT_VERSION} kubesplit \
	&& pip install --no-cache-dir kubesplit==${KUBESPLIT_VERSION}
