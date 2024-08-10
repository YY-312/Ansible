import subprocess

# Define the commands to be executed inside the container
commands = [
    "apt-get update",
    "apt-get install -y python3"
]

# Execute commands in the Docker container
for cmd in commands:
    full_cmd = f"docker exec clab-firstlab-apache-server bash -c '{cmd}'"
    subprocess.run(full_cmd, shell=True, check=True)
