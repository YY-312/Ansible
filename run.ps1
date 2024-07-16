# Initialize and apply OpenTofu configuration
tofu init
tofu apply -auto-approve

# Get the Apache container ID
$apache_container_id = tofu output -raw apache_container_id

# Create an Ansible variables file
"apache_container_id: $apache_container_id" | Out-File -FilePath apache_vars.yml

# Run the Ansible playbook
ansible-playbook -i inventory.txt -e @apache_vars.yml install_apache.yml
