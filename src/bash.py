import os
import subprocess

from src import config, util


def install_conda():
    """
    Install Miniconda if not already installed.

    This function checks if Miniconda is already installed. If not, it downloads
    the Miniconda installer, runs it in WSL, and then prints a success message.

    Returns:
        None
    """
    if verify_conda():
        print("Miniconda is already installed.")
        return

    # Download the Miniconda installer
    if not util.download_miniconda():
        print("Failed to download Miniconda installer.")
        exit()

    run_wsl_command(f"mkdir -p {config.CONDA_HOME}")
    run_wsl_command(f"bash miniconda.sh -b -s -t -u -p {config.CONDA_HOME}")
    run_wsl_command("rm miniconda.sh")
    run_wsl_command(f"{config.CONDA_HOME}/bin/conda init {config.DEFAULT_SHELL}")

    print("Miniconda installed successfully.")


def verify_conda():
    """
    Verify if Miniconda is already installed.

    This function checks if Miniconda is already installed by attempting to
    run the command 'conda --version' in WSL.

    Returns:
        bool: True if Miniconda is installed, False otherwise.
    """
    try:
        output = run_wsl_command("conda --version")
        return output is not None
    except subprocess.CalledProcessError:
        return False


def verify_env_setup():
    """
    Verify if the environment setup for Conda is done

    Returns:
        Tuple[bool, bool]: Tuple indicating whether Python 2 and Python 3 environments are set up.
    """
    has_py2 = run_wsl_command(f"conda activate {config.PYTHON2_ENV_NAME}")
    has_py3 = run_wsl_command(f"conda activate {config.PYTHON3_ENV_NAME}")

    return has_py2, has_py3


def setup_conda_env():
    """
    Setup Conda environments if not already set up
    """
    has_py2, has_py3 = verify_env_setup()

    if has_py2 is None:
        print("Creating Python 2.7 environment")
        run_wsl_command(f"conda create -n {config.PYTHON2_ENV_NAME} python=2.7 -y")

    if has_py3 is None:
        print("Creating Python 3.11 environment")
        run_wsl_command(f"conda create -n {config.PYTHON3_ENV_NAME} python=3.11 -y")

    print("Conda environment setup is now complete.")
    return


def init_datastore():
    """
    Initialize the datastore file if not present
    """
    return run_wsl_command(f"touch {config.DATASTORE_PATH}")


def update_rc_file():
    """
    Update the shell configuration file (e.g., .bashrc)
    """
    rc_contents = ["# >>> Google Cloud SDK Environment variables >>>\n"]
    rc_contents.append(
        f"export CLOUDSDK_DEV_PYTHON='{config.CONDA_HOME}/envs/{config.PYTHON2_ENV_NAME}/bin/python'\n"
    )
    rc_contents.append(f"export CLOUD_SDK_ROOT='{config.GCLOUD_HOME}'\n")
    rc_contents.append(
        f"export CLOUDSDK_PYTHON_HOME='{config.CONDA_HOME}/envs/{config.PYTHON3_ENV_NAME}'\n"
    )
    rc_contents.append(f"export CLOUDSDK_PYTHON='{config.CONDA_HOME}/envs/{config.PYTHON3_ENV_NAME}/bin/python'\n")
    rc_contents.append(f"export CLOUDSDK_DATASTORE='{config.DATASTORE_PATH}'\n")
    rc_contents.append("export APPLICATION_ID='dev~None'\n")
    rc_contents.append(
        'alias runapp="'
        + "python3 $CLOUD_SDK_ROOT/bin/dev_appserver.py"
        + " --runtime_python_path='python27=$CLOUDSDK_DEV_PYTHON,python3=$CLOUDSDK_PYTHON'"
        + " --python_virtualenv_path $CLOUDSDK_PYTHON_HOME"
        + " --datastore_path=$CLOUDSDK_DATASTORE"
        + '"\n'
    )
    rc_contents.append("# <<< Google Cloud SDK Environment variables <<<\n\n")

    with open("rc", "w") as f:
        f.writelines(rc_contents)

    run_wsl_command("sed -i -e 's/\r//g' rc")
    run_wsl_command(f"cat rc >> ~/.{config.DEFAULT_SHELL}rc")


def verify_gcloud():
    """
    Verify if Google Cloud SDK is installed
    """
    ...


def install_gcloud():
    """
    Install Google Cloud SDK if not already installed
    """
    if verify_gcloud():
        print("Gcloud is already installed.")
        return


def run_wsl_command(command):
    try:
        # Use 'wsl' command to run commands in WSL
        command_list = [
            "wsl",
            config.DEFAULT_SHELL,
            "-ic",
            f"source ~/.{config.DEFAULT_SHELL}rc && " + command,
        ]
        result = subprocess.run(
            command_list, capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None


def bash_main():
    """
    Linux part of the script.
    """
    print("Installing conda.")
    install_conda()
    print("\n----------------------------------------------------------------------\n")

    print("Setting up conda environment.")
    setup_conda_env()
    print("\n----------------------------------------------------------------------\n")

    print("Creating datastore file.")
    init_datastore()
    print("\n----------------------------------------------------------------------\n")

    print("Updating bashrc")
    update_rc_file()
    print("\n----------------------------------------------------------------------\n")

    print("Installing Google Cloud SDK")
    install_gcloud()
    print("\n----------------------------------------------------------------------\n")

    return


if __name__ == "__main__":
    bash_main()
