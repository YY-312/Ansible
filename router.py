import subprocess
import os

# Define the Python script content to be executed inside the container
python_script = """
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
            shell.send(f"{command}\\n")  # Correct usage of newline
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
        "hostname hi"   # Change the hostname to "helloOne"
    ]

    run_ssh_commands(commands)

if __name__ == "__main__":
    main()
"""

# Step 1: Write the Python script to a file
with open('router.py', 'w') as file:
    file.write(python_script)

# Step 2: Update package list and install necessary packages inside the container
subprocess.run(['docker', 'exec', '-i', '-u', 'root', 'clab-firstlab-csr-r1', 'bash', '-c', 'apt-get update && apt-get install -y python3 python3-pip'], check=True)

# Step 3: Install Paramiko if not already installed
subprocess.run(['docker', 'exec', '-i', '-u', 'root', 'clab-firstlab-csr-r1', 'bash', '-c', 'pip3 install paramiko'], check=True)

# Step 4: Copy the Python script into the Docker container
subprocess.run(['docker', 'cp', 'router.py', 'clab-firstlab-csr-r1:/router.py'], check=True)

# Step 5: Run the Python script inside the Docker container
subprocess.run(['docker', 'exec', '-i', '-u', 'root', 'clab-firstlab-csr-r1', 'bash', '-c', 'python3 /router.py'], check=True)

# Cleanup: Remove the script file from the local machine
os.remove('router.py')
