import typer
from rich import print


import subprocess


def verify_wsl():
    """
    Verify if WSL (Windows Subsystem for Linux) is enabled.

    Returns:
        bool: True if WSL is enabled, False otherwise.
    """
    try:
        # Run 'wsl --list' command to check if any distributions are listed
        output = subprocess.check_output(
            ["wsl", "--list"], stderr=subprocess.STDOUT, text=True
        )
        # If the output contains any distribution, WSL is enabled
        if output.strip():
            return True
        else:
            return False
    except FileNotFoundError:
        # 'wsl' command not found, indicating WSL is not enabled
        return False
    except subprocess.CalledProcessError:
        # 'wsl --list' command returned non-zero exit code, indicating WSL is not enabled
        return False


def install_wsl():
    """
    Install WSL if not already enabled
    """
    try:
        # Enable WSL through dism.exe command-line tool
        subprocess.run(
            [
                "dism",
                "/online",
                "/enable-feature",
                "/featurename:Microsoft-Windows-Subsystem-Linux",
                "/all",
                "/norestart",
            ],
            check=True,
        )
        print("WSL is successfully enabled.")
        return True
    except subprocess.CalledProcessError as e:
        # Error occurred while enabling WSL
        print(f"Failed to enable WSL: {e}")
        return False


def verify_arch():
    """
    Verify if Arch Linux is installed in WSL
    """
    ...


def install_arch():
    """
    Install Arch Linux in WSL if not already installed
    """
    ...


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


def start_installation():
    """
    Start the installation process
    """
    if not verify_wsl():
        print("WSL is not enabled. | Enabling WSL.")
        install_wsl()
        print("WSL has been enabled.")
    else:
        print("WSL is already enabled.")

    if not verify_arch():
        print("Installing Arch Linux in WSL.")
        install_arch()
        print("Arch Linux is now installed.")
    else:
        print("Arch Linux is already installed.")

    print("Entering Linux env")
    enter_linux_env()
    print("Linux environment has been loaded.")

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


def verify_components():
    """
    Verify all components after installation
    """
    ...


def main(install: bool = False, verify: bool = False):
    """
    Main function to handle command-line arguments and start installation/verification.
    :param install: Boolean flag to indicate if components should be installed.
    :param verify: Boolean flag to indicate if components should be verified.
    """
    if install and verify:
        start_installation()
        verify_components()
        return
    if install:
        return start_installation()
    if verify:
        return verify_components()
    print(":wave: Welcome to the installer. Enter --help to begin.")
    return


if __name__ == "__main__":
    typer.run(main)
