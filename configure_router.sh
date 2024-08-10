#!/bin/bash

# Update and install required packages
#apt update && apt install -y python3 python3-pip telnet vim

# Install Python packages
#pip3 install ansible ansible-pylibssh

# Install packages in the container
docker exec -it clab-firstlab-csr-r1 bash -c 'apt update && apt install -y python3-pip telnet vim && pip3 install ansible ansible-pylibssh'

# Create ansible.cfg in /
docker exec -it clab-firstlab-csr-r1 bash -c 'cat <<EOF > /ansible.cfg
[defaults]
inventory = /inventory.yml
host_key_checking = False
timeout = 30

[privilege_escalation]
become = True
become_method = enable

[ssh_connection]
# Ensure SSH connections are configured properly
transport = network_cli
EOF'

# Create inventory.yml in /
docker exec -it clab-firstlab-csr-r1 bash -c 'cat <<EOF > /inventory.yml
all:
  hosts:
    csr1000v:
      ansible_host: 127.0.0.1
      ansible_user: admin
      ansible_password: admin
      ansible_connection: network_cli
      ansible_network_os: ios
      ansible_become: yes
      ansible_become_method: enable
EOF'

# Create configure_router.yml in /
docker exec -it clab-firstlab-csr-r1 bash -c 'cat <<EOF > /configure_router.yml
- name: Configure Router
  hosts: csr1000v
  gather_facts: no
  connection: network_cli
  tasks:
    - name: Set hostname
      ios_config:
        lines:
          - hostname yanyan
    - name: Ensure SSH is enabled
      ios_config:
        lines:
          - ip domain-name example.com
          - crypto key generate rsa modulus 2048
          - ip ssh version 2
          - line vty 0 4
          - transport input ssh
          - login local
EOF'

# Run Ansible playbook
docker exec -it clab-firstlab-csr-r1 bash -c "ansible-playbook -i /inventory.yml /configure_router.yml"
