# Function to enable WSL
function Install-WSL {
    Write-Host "Enabling WSL on the machine."
    try {
        # Enable WSL using dism.exe command-line tool
        & dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart > $null

        # Set WSL default version to 2
        & wsl --set-default-version 2 > $null

        Write-Host "WSL is successfully enabled."
    } catch {
        Write-Host "Failed to enable WSL: $_"
        exit 1
    }
}
# Function to download a file with multiple connections
function Download-File {
    param (
        [string]$url,
        [string]$outputPath
    )

    # Create a web request object
    $webRequest = [System.Net.HttpWebRequest]::Create($url)
    
    # Set the number of connections (threads) for download
    $webRequest.ServicePoint.ConnectionLimit = 10
    
    # Get the web response
    $webResponse = $webRequest.GetResponse()
    
    # Create a file stream to save the downloaded file
    $fileStream = [System.IO.File]::Create($outputPath)

    # Get the response stream
    $responseStream = $webResponse.GetResponseStream()

    # Buffer size for reading the response stream
    $bufferSize = 8192
    $buffer = New-Object byte[] $bufferSize

    # Read from the response stream and write to the file stream
    $bytesRead = $responseStream.Read($buffer, 0, $bufferSize)
    while ($bytesRead -gt 0) {
        $fileStream.Write($buffer, 0, $bytesRead)
        $bytesRead = $responseStream.Read($buffer, 0, $bufferSize)
    }

    # Close the streams
    $fileStream.Close()
    $responseStream.Close()
}

# Function to verify if WSL is enabled
function Verify-WSL {
    # Check if the 'wsl' command is available
    if (!(Get-Command wsl -ErrorAction SilentlyContinue)) {
        exit 1
    }

    # Check if any distributions are listed
    $wslList = & wsl --list 2>&1
    if ($LASTEXITCODE -ne 0 -or $wslList -eq $null) {
        exit 1
    }
}

# Function to install Arch Linux in WSL
function Install-ArchLinux {
    Write-Host "Installing Arch Linux in WSL."
    
    # Download Arch Linux ZIP file
    $url = "https://github.com/yuk7/ArchWSL/releases/download/24.3.11.0/Arch.zip"
    $outputPath = "arch.zip"
    Download-File -url $url -outputPath $outputPath

    # Extract the ZIP file
    $extractPath = "arch_files"
    Expand-Archive -Path $outputPath -DestinationPath $extractPath

    # Change directory to the extracted folder
    Set-Location -Path $extractPath

    # Rename to tummee.exe
    Rename-Item -Path ".arch.exe" -NewName ".\tummee.exe"

    # Execute arch.exe
    & .\tummee.exe

    Write-Host "Arch Linux installation completed successfully."
}

# Main function
function Main {
    try {
        Install-WSL
        Verify-WSL
        Install-ArchLinux
    } catch {
        Write-Host "An error occurred: $_"
        exit 1
    }
}

Main
