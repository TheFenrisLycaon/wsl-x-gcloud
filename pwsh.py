import os
import subprocess

# Import configuration and utility modules
from src import config, util


def install_wsl():
    """
    Install WSL (Windows Subsystem for Linux) if not already enabled.

    This function enables WSL using the dism.exe command-line tool and sets it as the default version.

    Returns:
        None
    """
    if verify_wsl():
        print("WSL is already enabled.")
        return

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

        # Set WSL default version to 2
        subprocess.run(["wsl", "--set-default-version", "2"])
        return
    except subprocess.CalledProcessError as e:
        # Error occurred while enabling WSL
        print(f"Failed to enable WSL: {e}")
        return


def verify_wsl():
    """
    Verify if WSL (Windows Subsystem for Linux) is enabled.

    This function checks if WSL is enabled by running the 'wsl --list' command.

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


def install_arch():
    """
    Install Arch Linux in WSL.

    This function downloads and installs Arch Linux in WSL.

    Returns:
        None
    """
    if verify_arch():
        print("Arch Linux is already installed.")
        return

    # Download the Arch Linux zip file
    if not util.download_arch_linux():
        print("Failed to download Arch Linux zip file.")
        exit()

    # Extract the downloaded zip file
    if not util.extract_zip(config.ARCH_LINUX_ZIP_FILENAME, config.ARCH_LINUX_DIR):
        print("Failed to extract Arch Linux zip file.")
        exit()

    # Change directory to the extracted folder
    os.chdir(config.ARCH_LINUX_DIR)

    # Run the arch.exe executable
    try:
        subprocess.run(["./arch.exe"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running arch.exe: {e}")
        exit()

    print("Arch Linux installed successfully.")
    return


def verify_arch():
    """
    Verify if Arch Linux is installed in WSL.

    This function checks if Arch Linux is installed in WSL by looking for '/usr/bin/pacman' file.

    Returns:
        bool: True if Arch Linux is installed, False otherwise.
    """
    try:
        # Run a command in WSL to check if a specific file or directory exists
        subprocess.run(
            ["wsl", "ls", "/usr/bin/pacman"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        # If the command succeeds, it means Arch Linux is installed
        return True
    except subprocess.CalledProcessError:
        # If the command fails (returns non-zero exit code), Arch Linux is not installed
        return False


def main():
    """
    This function enables WSL on the machine and installs Arch Linux in WSL.
    """
    print("Enabling WSL on the machine.")
    install_wsl()

    print("Installing Arch Linux in WSL.")
    install_arch()


if __name__ == "__main__":
    main()
