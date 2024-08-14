import subprocess

def run_command_in_container(container_name, command):
    """Function to run shell commands inside a Docker container."""
    full_command = f"docker exec {container_name} bash -c \"{command}\""
    result = subprocess.run(full_command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Command '{command}' executed successfully in container '{container_name}'.")
    else:
        print(f"Error executing '{command}' in container '{container_name}': {result.stderr}")
        raise Exception(result.stderr)

def configure_ssl_on_apache(container_name):
    # Rename and move SSL certificate
    run_command_in_container(container_name, "cp /usr/local/apache2/conf/ssl/apache.crt /usr/local/apache2/conf/server.crt")

    # Rename and move SSL key
    run_command_in_container(container_name, "cp /usr/local/apache2/conf/ssl/apache.key /usr/local/apache2/conf/server.key")

    # Update httpd-ssl.conf with SSL settings
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
    run_command_in_container(container_name, f"echo '{ssl_conf_content}' > /usr/local/apache2/conf/extra/httpd-ssl.conf")

    # Include httpd-ssl.conf in main configuration
    run_command_in_container(container_name, "echo 'Include conf/extra/httpd-ssl.conf' >> /usr/local/apache2/conf/httpd.conf")

    # Load SSL and socache_shmcb modules
    run_command_in_container(container_name, "echo 'LoadModule ssl_module modules/mod_ssl.so' >> /usr/local/apache2/conf/httpd.conf")
    run_command_in_container(container_name, "echo 'LoadModule socache_shmcb_module modules/mod_socache_shmcb.so' >> /usr/local/apache2/conf/httpd.conf")

    # Restart Apache to apply changes
    run_command_in_container(container_name, "apachectl restart")

if __name__ == "__main__":
    configure_ssl_on_apache("clab-firstlab-apache-server")
