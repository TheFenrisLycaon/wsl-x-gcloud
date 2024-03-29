import os
import zipfile

import requests
from tqdm import tqdm

import src.config as config


def extract_zip(zip_file, extract_to):
    """
    Extract a zip file to the specified directory.
    Args:
        zip_file (str): Path to the zip file to be extracted.
        extract_to (str): Directory where the contents of the zip file will be extracted.

    Returns:
        bool: True if extraction is successful, False otherwise.
    """
    try:
        print(f"Extracting zip file: {zip_file} to: {extract_to}")
        # Open the zip file
        with zipfile.ZipFile(zip_file, "r") as zip_ref:
            # Extract all contents to the specified directory
            zip_ref.extractall(extract_to)
        print(f"Successfully extracted {zip_file} to {extract_to}")
        return True
    except Exception as e:
        # Handle any other exceptions
        print(f"An unexpected error occurred: {e}")
        return False


def download_file(url, destination):
    """
    Download a file from the specified URL and save it to the destination.

    Args:
        url (str): The URL of the file to download.
        destination (str): The path where the downloaded file will be saved.

    Returns:
        bool: True if the file is successfully downloaded, False otherwise.
    """
    try:
        # Check if the file already exists
        if os.path.exists(destination):
            print(f"File already exists: {destination}")
            return True

        # Send a GET request to the URL to download the file
        # Use stream=True to download in chunks
        response = requests.get(url, stream=True)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Get the total file size from the Content-Length header
            total_size = int(response.headers.get("content-length", 0))
            # Initialize a progress bar with the total file size
            progress_bar = tqdm(total=total_size, unit="B", unit_scale=True)
            # Open the destination file in binary write mode
            with open(destination, "wb") as f:
                # Iterate over the response content in chunks and write to the file
                for chunk in response.iter_content(chunk_size=1024):
                    f.write(chunk)
                    # Update the progress bar with the number of bytes written
                    progress_bar.update(len(chunk))
            # Close the progress bar after finishing the download
            progress_bar.close()
            print(f"File downloaded successfully to: {destination}")
            return True
        else:
            print(f"Failed to download file: HTTP status code {response.status_code}")
            return False
    except Exception as e:
        # Handle any errors that occur during the download process
        print(f"Error downloading file: {e}")
        return False


def download_arch_linux():
    """
    Download the Arch Linux zip file from the URL specified in the TOML config file.

    Returns:
        bool: True if the zip file is successfully downloaded, False otherwise.
    """
    try:
        # Assuming CONFIG is a global variable containing necessary configuration
        return download_file(config.ARCH_LINUX_ZIP_URL, config.ARCH_LINUX_ZIP_FILENAME)
    except Exception as e:
        # Handle any errors that occur during the download process
        print(f"Error downloading Arch Linux: {e}")
        return False


def download_miniconda():
    """
    Download the Miniconda installer from the URL specified in the configuration.

    Returns:
        bool: True if the installer is successfully downloaded, False otherwise.
    """
    try:
        # Assuming CONFIG is a global variable containing necessary configuration
        return download_file(config.MINICONDA_URL, config.MINICONDA_FILE)
    except Exception as e:
        # Handle any errors that occur during the download process
        print(f"Error downloading Miniconda: {e}")
        return False
