!#/usr/sbin/bash

# Set options for error handling
set -eu

# Define environment variables
CONDAHOME="$HOME/.condahome"        # Path to Conda home directory
PYTHON2_ENV_NAME="Tummee_PY2"        # Name of Python 2 environment
PYTHON3_ENV_NAME="Tummee_PY3"        # Name of Python 3 environment

# Get the name of the current shell
shell_name="bash"      # Retrieve the name of the current shell

verify_conda() {
    # Check if Conda is installed by running 'conda --version'
    if conda --version >/dev/null 2>&1; then
        # Conda is installed, return success (0)
        return 0
    else
        # Conda is not installed, return failure (1)
        return 1
    fi
}

install_conda() {
    # Check if Miniconda is already installed
    if verify_conda; then
        echo "Miniconda is already installed."
        return
    fi

    # Create Conda home directory if it doesn't exist
    mkdir -p $HOME/.condahome

    # Download Miniconda installer
    curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

    mv ./Miniconda3-latest-Linux-x86_64.sh ~/miniconda.sh

    # Run Miniconda installer
    bash $HOME/miniconda.sh -b -s -u -p $CONDAHOME

    # Remove Miniconda installer
    rm $HOME/miniconda.sh

    # Initialize Conda in the current shell
    $CONDAHOME/bin/conda init $shell_name

    # Print success message
    echo "Miniconda installed successfully."
}

verify_env_setup() {
    # Check if Python 2 environment is activated
    has_py2=$(conda activate $PYTHON2_ENV_NAME >/dev/null 2>&1 && echo "yes" || echo "no")

    # Check if Python 3 environment is activated
    has_py3=$(conda activate $PYTHON3_ENV_NAME >/dev/null 2>&1 && echo "yes" || echo "no")

    # Return true if both Python 2 and Python 3 environments are activated, false otherwise
    [[ "$has_py2" == "yes" && "$has_py3" == "yes" ]]
}

setup_conda_env() {
    # Verify if Python environments are already set up
    verify_env_setup || {
        # If not set up, create Python 2.7 environment
        echo "Creating Python 2.7 environment"
        conda create -n $PYTHON2_ENV_NAME python=2.7 -y

        # Create Python 3.11 environment
        echo "Creating Python 3.11 environment"
        conda create -n $PYTHON3_ENV_NAME python=3.11 -y
    }

    # Print completion message
    echo "Conda environment setup is now complete."
}

update_rc_file() {

    touch $HOME/.bashrc	

    # Append to the .bashrc file using a here document
    cat >>"$HOME/.bashrc" <<'EOF'
# >>> Google Cloud SDK Environment variables >>>
export CONDAHOME="$HOME/.condahome"   
export PYTHON2_ENV_NAME="Tummee_PY2"        
export PYTHON3_ENV_NAME="Tummee_PY3"        
export CLOUDSDK_DEV_PYTHON="$CONDAHOME/envs/$PYTHON2_ENV_NAME/bin/python"
export CLOUD_SDK_ROOT="$HOME/google-cloud-sdk"
export CLOUDSDK_PYTHON_HOME="$CONDAHOME/envs/$PYTHON3_ENV_NAME"
export CLOUDSDK_PYTHON="$CONDAHOME/envs/$PYTHON3_ENV_NAME/bin/python"
export CLOUDSDK_DATASTORE="$HOME/datastore.filestub"
export APPLICATION_ID='dev~None'
alias runapp='python3 $CLOUD_SDK_ROOT/bin/dev_appserver.py --runtime_python_path="python27=$CLOUDSDK_DEV_PYTHON,python3=$CLOUDSDK_PYTHON" --python_virtualenv_path $CLOUDSDK_PYTHON_HOME --datastore_path=$CLOUDSDK_DATASTORE'
# <<< Google Cloud SDK Environment variables <<<

EOF
}

install_gcloud() {
    echo "Downloading Google Cloud SDK..."
    curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-470.0.0-linux-x86_64.tar.gz

    echo "Extracting Google Cloud SDK..."
    mkdir -p $HOME/google-cloud-sdk
    tar -xf google-cloud-cli-470.0.0-linux-x86_64.tar.gz -C $HOME

    rm ./google-cloud-cli-470.0.0-linux-x86_64.tar.gz

    echo "Installing Google Cloud SDK..."
    # Run the Google Cloud SDK installation script quietly
    $HOME/google-cloud-sdk/install.sh -q
    
    echo "Initializing Google Cloud SDK..."
    # Initialize gcloud
    $HOME/google-cloud-sdk/bin/gcloud init --skip-diagnostics
    
    echo "Google Cloud SDK installed successfully."
}


bash_main() {
    touch $HOME/.bashrc

    # Call install_conda function to install Conda
    echo "Installing Conda."
    install_conda
     
    # Source .bashrc to ensure environment changes from conda take effect
    source $HOME/.bashrc

    # Call setup_conda_env function to set up Conda environments
    echo "Setting up Conda environment."
    setup_conda_env
    
    # Update .bashrc file with Google Cloud SDK environment variables and aliases
    echo "Updating .bashrc."
    update_rc_file

    # # Source .bashrc to apply changes
    source $HOME/.bashrc  

    # Create a datastore file
    echo "Creating datastore file."
    touch $CLOUDSDK_DATASTORE
    
    # Call install_gcloud function to install Google Cloud SDK
    echo "Installing Google Cloud SDK."
    install_gcloud
}


bash_main
