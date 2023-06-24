APP_NAME ?= kubesplit

MK_ACTIONLINT_SHA256          := fbbf3b567ac9854481cf32274f480c501f093d9436151e50d584ed89bc2afdcc
MK_COMMON_SHA256              := 2d49615c5fa43b30d739e4a00c175fc7f295665c9a01f32a52792f6aa80a3bfa
MK_DOCKER_SHA256              := 8dddb0f5b71d24b4b205a36f514aa7c9ddd4ca771557694e6d1410c5fbbdf8f2
MK_MDLINT_SHA256              := 7ddab45f6476376dc8b05cbb2970716b94d297f3d30bae94e593b543b0e53440
MK_PRE_COMMIT_SHA256          := 0c73900d816a266dfaa230b3223f25f53caff97d102e8fced7dbab997c2a46f1
MK_PYTHON_POETRY_APP_SHA256   := 318b8ebede6324bee2cd10adfcd2672389e25333fa2f13d5ed5e480a3630bd1c
MK_PYTHON_POETRY_VENV_SHA256  := ed1513b743db40823c7f4432dd6b46749f80abf4ada1ecc95ba1e9c52e6f6274

MK_GIT_REF ?= mk-1.4.0

include toolbox/mk/remote-mk.mk

include generated/mk/common.mk
include generated/mk/actionlint.mk
include generated/mk/pre-commit.mk
include generated/mk/python-poetry-venv.mk
include generated/mk/python-poetry-app.mk
include generated/mk/docker.mk
include generated/mk/mdlint.mk
