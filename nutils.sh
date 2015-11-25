#!/bin/sh -e

NUTILS_EXE_PATH="$(readlink -e "${0}")"
NUTILS_EXE_NAME="$(basename "${NUTILS_EXE_PATH}")"
NUTILS_EXE_DIR="$(dirname "${NUTILS_EXE_PATH}")"
EXE_DIR="$(cd "$(dirname "${0}")" && pwd)"
EXE_NAME="$(basename "${0}")"
EXE_PATH="${EXE_DIR}/${EXE_NAME}"
PY_PATH="${EXE_DIR}/$(echo "${EXE_NAME}" | cut -c3-).py"
PY_ENV="${EXE_DIR}/py3env"
PY_REQ="${EXE_DIR}/requirements.txt"

test "${EXE_PATH}" = "${NUTILS_EXE_PATH}" && echo "This script is meant to be symlinked" && false
test ! "$(echo "${EXE_NAME}" | cut -c1-2)" = "n-" && echo "Symlinks to '${NUTILS_EXE_NAME}' must start with 'n-'" && false
test ! -f "${PY_PATH}" && echo "'${PY_PATH}' not found" && false

if [ -f "${PY_REQ}" ]
then
  if [ ! -f "${PY_ENV}/bin/activate" ]
  then
    virtualenv -p python3 "${PY_ENV}"
    sed -i '4 i\VIRTUAL_ENV_DISABLE_PROMPT=1\n' "${PY_ENV}/bin/activate"
    pip install -r "${PY_REQ}"
  fi

  . "${PY_ENV}/bin/activate"
fi

exec python3 "${PY_PATH}"
