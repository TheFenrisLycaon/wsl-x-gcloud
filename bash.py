# linux_part.py

import os
import subprocess

from src import config, util


def verify_conda():
    """
    Verify if Conda (Anaconda/Miniconda) is installed
    """
    ...


def install_conda():
    """
    Install Conda if not already installed
    """
    ...


def verify_env_setup():
    """
    Verify if the environment setup for Conda is done
    """
    ...


def setup_conda_env():
    """
    Setup Conda environments if not already set up
    """
    ...


def verify_datastore_file():
    """
    Verify if the datastore file is present
    """
    ...


def init_datastore():
    """
    Initialize the datastore file if not present
    """
    ...


def enter_linux_env():
    """
    Enter Linux environment (WSL)
    """
    ...


def switch_to_bash():
    """
    Switch from PowerShell/CMD to the Bash environment.
    """
    try:
        # Execute the wsl command to switch to the WSL environment
        os.system("wsl bash")
    except subprocess.CalledProcessError as e:
        print(f"Error switching to Bash: {e}")
        exit()

    return


def update_rc_file():
    """
    Update the shell configuration file (e.g., .bashrc)
    """
    ...


def verify_gcloud():
    """
    Verify if Google Cloud SDK is installed
    """
    ...


def install_gcloud():
    """
    Install Google Cloud SDK if not already installed
    """
    ...


def reload_shell():
    """
    Reload the shell to apply configuration changes
    """
    ...


def linux_part():
    """
    Linux part of the script.
    """
    if not verify_conda():
        print("Installing conda.")
        install_conda()
        print("Conda is now installed.")
    else:
        print("Conda is already installed.")

    if not verify_env_setup():
        print("Setting up conda environment.")
        setup_conda_env()
        print("Conda environments have been setup.")
    else:
        print("Conda env is already setup.")

    reload_shell()

    if not verify_datastore_file():
        print("Creating datastore file.")
        init_datastore()
        print("Datastore file is created.")
    else:
        print("Datastore file is already present.")

    print("Updating bashrc")
    update_rc_file()
    reload_shell()
    print("bashrc updated with configs.")

    if not verify_gcloud():
        print("Gcloud is not installed. | Installing gcloud.")
        install_gcloud()
        print("Gcloud installed.")
    else:
        print("Gcloud is already installed.")


if __name__ == "__main__":
    linux_part()
