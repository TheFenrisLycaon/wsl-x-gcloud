import subprocess


def main():
    # Execute the PowerShell part
    subprocess.run(["python", "pwsh.py"], check=True)

    # # Execute the Linux part
    # subprocess.run(["python", "bash.py"], check=True)


if __name__ == "__main__":
    main()
