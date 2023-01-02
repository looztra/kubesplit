APP_NAME ?= kubesplit

MK_ACTIONLINT_SHA256          := fbbf3b567ac9854481cf32274f480c501f093d9436151e50d584ed89bc2afdcc
MK_COMMON_SHA256              := 2d49615c5fa43b30d739e4a00c175fc7f295665c9a01f32a52792f6aa80a3bfa
MK_DOCKER_SHA256              := 8dddb0f5b71d24b4b205a36f514aa7c9ddd4ca771557694e6d1410c5fbbdf8f2
MK_PRE_COMMIT_SHA256          := 0c73900d816a266dfaa230b3223f25f53caff97d102e8fced7dbab997c2a46f1
MK_PYTHON_POETRY_APP_SHA256   := 65204fedf5a5bfe1915f55b2af9414f9aa65e26d0c0da84a695964ded8129b48
MK_PYTHON_POETRY_VENV_SHA256  := 9cf4d57d6acea5bf2dcd2e0bf4b771528ae2a4c4dfc492188d09c7eaee2c8014

MK_GIT_REF ?= chore/mk/new-targets

include toolbox/mk/remote-mk.mk

include generated/mk/common.mk
include generated/mk/actionlint.mk
include generated/mk/pre-commit.mk
include generated/mk/python-poetry-venv.mk
include generated/mk/python-poetry-app.mk
include generated/mk/docker.mk
