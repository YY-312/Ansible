#!/bin/bash

# Define the Python script content
PYTHON_SCRIPT=$(cat <<EOF
import paramiko
import time

def run_ssh_commands(commands):
    host = "127.0.0.1"
    port = 22
    username = "admin"
    password = "admin"

    # Create an SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to the router
        ssh.connect(host, port, username, password)

        # Start an interactive shell session
        shell = ssh.invoke_shell()

        # Run the commands
        for command in commands:
            shell.send(f"{command}\n")  # Correct usage of newline
            time.sleep(1)  # Wait for the command to execute

        # Read the output from the shell
        output = shell.recv(10000).decode('utf-8')
        print(output)

    except paramiko.AuthenticationException:
        print("Authentication failed.")
    except paramiko.SSHException as e:
        print(f"SSH error: {e}")
    finally:
        # Close the SSH connection
        ssh.close()

def main():
    commands = [
        "enable",             # Enter enable mode
        "configure terminal", # Enter global configuration mode
        "hostname helloabigail"    # Change the hostname to "helloyy"
    ]

    run_ssh_commands(commands)

if __name__ == "__main__":
    main()
EOF
)

# Step 1: Create the Python script inside the container
sudo docker exec -i -u root clab-firstlab-csr-r1 bash -c "echo '$PYTHON_SCRIPT' > /root/router.py"

# Step 2: Install Paramiko if it's not already installed
sudo docker exec -i -u root clab-firstlab-csr-r1 bash -c "pip3 install paramiko"

# Step 3: Run the Python script inside the container
sudo docker exec -i -u root clab-firstlab-csr-r1 bash -c "python3 /root/router.py"
