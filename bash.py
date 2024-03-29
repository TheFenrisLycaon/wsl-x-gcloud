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

    # Run the Miniconda installer
    # TODO: Testing pending.
    try:
        run_wsl_command("./Miniconda3-latest-Linux-x86_64.sh")
    except subprocess.CalledProcessError as e:
        print(f"Error installing Miniconda: {e}")
        exit()

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
    """
    ...


def setup_conda_env():
    """
    Setup Conda environments if not already set up
    """
    if verify_env_setup():
        print("Conda environment is alredy setup.")
        return


def verify_datastore_file():
    """
    Verify if the datastore file is present
    """
    ...


def init_datastore():
    """
    Initialize the datastore file if not present
    """
    if verify_datastore_file():
        print("A datastore file is already present.")
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
        print(f"Error executing command '{' '.join(command_list)}' in WSL: {e}")
        return None


def linux_part():
    """
    Linux part of the script.
    """
    print("Installing conda.")
    install_conda()

    print("Setting up conda environment.")
    setup_conda_env()

    print("Creating datastore file.")
    init_datastore()

    print("Updating bashrc")
    update_rc_file()

    print("Installing Google Cloud SDK")
    install_gcloud()

    return


if __name__ == "__main__":
    linux_part()
