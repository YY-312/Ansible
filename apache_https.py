import subprocess
 
def run_command_in_container(container_name, command):

    """Function to run shell commands inside a Docker container without using bash."""

    docker_command = f"docker exec {container_name} {command}"

    result = subprocess.run(docker_command, shell=True, capture_output=True, text=True)

    if result.returncode == 0:

        print(f"Command '{command}' executed successfully in container '{container_name}'.")

    else:

        print(f"Error executing '{command}' in container '{container_name}': {result.stderr}")

        raise Exception(result.stderr)
 
def configure_ssl_on_apache(container_name):

    # Ensure the extra directory exists

    run_command_in_container(container_name, "mkdir -p /usr/local/apache2/conf/extra")
 
    # Rename and move SSL certificate

    run_command_in_container(container_name, "cp /usr/local/apache2/conf/ssl/apache.crt /usr/local/apache2/conf/server.crt")
 
    # Rename and move SSL key

    run_command_in_container(container_name, "cp /usr/local/apache2/conf/ssl/apache.key /usr/local/apache2/conf/server.key")
 
    # Debug: List contents of /usr/local/apache2/conf to ensure it exists

    run_command_in_container(container_name, "ls -l /usr/local/apache2/conf")
 
    # Debug: Check if httpd.conf exists

    run_command_in_container(container_name, "ls /usr/local/apache2/conf/httpd.conf")
 
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

    # Append SSL configuration to httpd-ssl.conf

    run_command_in_container(container_name, f"bash -c 'echo \"{ssl_conf_content}\" >> /usr/local/apache2/conf/extra/httpd-ssl.conf'")
 
    # Include httpd-ssl.conf in main configuration if not already included

    include_directive = "Include conf/extra/httpd-ssl.conf"

    run_command_in_container(container_name, f"grep -qxF '{include_directive}' /usr/local/apache2/conf/httpd.conf || echo '{include_directive}' >> /usr/local/apache2/conf/httpd.conf")
 
    # Load SSL and socache_shmcb modules if not already loaded

    ssl_module = "LoadModule ssl_module modules/mod_ssl.so"

    socache_module = "LoadModule socache_shmcb_module modules/mod_socache_shmcb.so"

    run_command_in_container(container_name, f"grep -qxF '{ssl_module}' /usr/local/apache2/conf/httpd.conf || echo '{ssl_module}' >> /usr/local/apache2/conf/httpd.conf")

    run_command_in_container(container_name, f"grep -qxF '{socache_module}' /usr/local/apache2/conf/httpd.conf || echo '{socache_module}' >> /usr/local/apache2/conf/httpd.conf")
 
    # Restart Apache to apply changes

    run_command_in_container(container_name, "apachectl restart")
 
if __name__ == "__main__":

    container_name = "clab-firstlab-apache-server"

    configure_ssl_on_apache(container_name)
