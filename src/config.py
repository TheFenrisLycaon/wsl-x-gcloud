WSL_USER = "fenris"
if WSL_USER == "root":
    USER_HOME = "/root"
else:
    USER_HOME = f"/home/{WSL_USER}"

DEFAULT_SHELL = "bash"

ARCH_LINUX_ZIP_URL = "https://github.com/yuk7/ArchWSL/releases/download/24.3.11.0/Arch.zip"
ARCH_LINUX_ZIP_FILENAME = "arch.zip"
ARCH_LINUX_DIR = "arch"

MINICONDA_URL = "https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"
MINICONDA_FILE = "miniconda.sh"

CONDA_HOME = f"{USER_HOME}/.condahome"
PYTHON2_ENV_NAME = "Tummee_PY2"
PYTHON3_ENV_NAME = "Tummee_PY3"

DATASTORE_PATH = f"{USER_HOME}/datastore.bin"

GCLOUD_HOME = f"{USER_HOME}/google-cloud-sdk"
