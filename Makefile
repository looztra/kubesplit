APP_NAME      ?= kubesplit
LOCAL_MK_ROOT ?= toolbox/mk


include $(LOCAL_MK_ROOT)/common.mk
include $(LOCAL_MK_ROOT)/mdlint.mk
include $(LOCAL_MK_ROOT)/pre-commit.mk
include $(LOCAL_MK_ROOT)/python-uv-extras.mk
include $(LOCAL_MK_ROOT)/python-base-venv.mk
include $(LOCAL_MK_ROOT)/python-uv-venv.mk
include $(LOCAL_MK_ROOT)/python-base-app.mk
include $(LOCAL_MK_ROOT)/python-uv-app.mk
