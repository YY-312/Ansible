import subprocess

def run_command_in_container(container, command):
    """Function to run shell commands inside a Docker container."""
    docker_command = f"docker exec {container} bash -c '{command}'"
    result = subprocess.run(docker_command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Command '{docker_command}' executed successfully.")
    else:
        print(f"Error executing '{docker_command}': {result.stderr}")
        raise Exception(result.stderr)

def configure_ssl_on_apache(container_name):
    # Create necessary directories
    run_command_in_container(container_name, "mkdir -p /usr/local/apache2/conf/extra")

    # Rename and move SSL certificate
    run_command_in_container(container_name, "cp /usr/local/apache2/conf/ssl/apache.crt /usr/local/apache2/conf/server.crt")

    # Rename and move SSL key
    run_command_in_container(container_name, "cp /usr/local/apache2/conf/ssl/apache.key /usr/local/apache2/conf/server.key")

    # Update httpd-ssl.conf with SSL settings
    ssl_conf_path = "/usr/local/apache2/conf/extra/httpd-ssl.conf"
    ssl_conf_content = """
ServerName 192.168.2.2
<IfModule ssl_module>
    Listen 443
    SSLPassPhraseDialog  builtin
    SSLSessionCache       shmcb:/usr/local/apache2/logs/ssl_scache(512000)
    SSLSessionCacheTimeout  300
    SSLMutex  file:/usr/local/apache2/logs/ssl_mutex
    SSLCertificateFile "/usr/local/apache2/conf/server.crt"
    SSLCertificateKeyFile "/usr/local/apache2/conf/server.key"
    <VirtualHost _default_:443>
        ServerAdmin webmaster@localhost
        DocumentRoot "/usr/local/apache2/htdocs"
        ErrorLog "logs/ssl_error_log"
        CustomLog "logs/ssl_access_log" common
        SSLEngine on
    </VirtualHost>
</IfModule>
"""

    # Append SSL configuration to httpd-ssl.conf
    run_command_in_container(container_name, f"bash -c 'echo \"{ssl_conf_content}\" >> {ssl_conf_path}'")

    # Include httpd-ssl.conf in main configuration if not already included
    httpd_conf_path = "/usr/local/apache2/conf/httpd.conf"
    include_directive = "Include conf/extra/httpd-ssl.conf"
    run_command_in_container(container_name, f"bash -c 'grep -qxF \"{include_directive}\" {httpd_conf_path} || echo \"{include_directive}\" >> {httpd_conf_path}'")

    # Load SSL and socache_shmcb modules if not already loaded
    ssl_module = "LoadModule ssl_module modules/mod_ssl.so"
    socache_module = "LoadModule socache_shmcb_module modules/mod_socache_shmcb.so"
    run_command_in_container(container_name, f"bash -c 'grep -qxF \"{ssl_module}\" {httpd_conf_path} || echo \"{ssl_module}\" >> {httpd_conf_path}'")
    run_command_in_container(container_name, f"bash -c 'grep -qxF \"{socache_module}\" {httpd_conf_path} || echo \"{socache_module}\" >> {httpd_conf_path}'")

    # Restart Apache to apply changes
    run_command_in_container(container_name, "apachectl restart")

if __name__ == "__main__":
    container_name = "clab-firstlab-apache-server"
    configure_ssl_on_apache(container_name)
