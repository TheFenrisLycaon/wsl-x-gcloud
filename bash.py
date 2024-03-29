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
        run_wsl_command(f"conda create -n {config.PYTHON2_ENV_NAME} python=2.7")

    if has_py3 is None:
        run_wsl_command(f"conda create -n {config.PYTHON3_ENV_NAME} python=3.11")

    print("Conda environment setup is now complete.")
    return


def init_datastore():
    """
    Initialize the datastore file if not present
    """
    return run_wsl_command(f"touch {config.DATASTORE_PATH}")


def append_line_to_file(line, filepath):
    """
    Append a line to a file if it doesn't already exist.

    Args:
        line (str): The line to append to the file.
        filepath (str): The path to the file.

    Returns:
        bool: True if the line is appended, False if the line already exists in the file.
    """
    # Check if the line already exists in the file
    output = run_wsl_command(f"grep -qx '{line}' {filepath} && echo 1 || echo 0")

    if output is None:
        output = "0"

    # If the line doesn't exist, append it to the file
    if output.strip() == "0":
        run_wsl_command(f'echo "{line}" >> {filepath}')
        print(f"Line '{line}' appended to {filepath}")
        return True
    else:
        print(f"Line '{line}' already exists in {filepath}")
        return False


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
        print(f"Error executing command {' '.join(command_list)} in WSL")
        return None


def bash_main():
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
    bash_main()
