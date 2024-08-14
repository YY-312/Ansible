import subprocess

def run_command(command):
    """Function to run shell commands."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Command '{command}' executed successfully.")
    else:
        print(f"Error executing '{command}': {result.stderr}")
        raise Exception(result.stderr)

def configure_ssl_on_apache():
    # Rename and move SSL certificate
    run_command("cp /usr/local/apache2/conf/ssl/apache.crt /usr/local/apache2/conf/server.crt")

    # Rename and move SSL key
    run_command("cp /usr/local/apache2/conf/ssl/apache.key /usr/local/apache2/conf/server.key")

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
    with open("/usr/local/apache2/conf/extra/httpd-ssl.conf", "w") as ssl_conf_file:
        ssl_conf_file.write(ssl_conf_content)

    # Include httpd-ssl.conf in main configuration
    with open("/usr/local/apache2/conf/httpd.conf", "a") as httpd_conf_file:
        httpd_conf_file.write("\nInclude conf/extra/httpd-ssl.conf\n")

    # Load SSL and socache_shmcb modules
    with open("/usr/local/apache2/conf/httpd.conf", "a") as httpd_conf_file:
        httpd_conf_file.write("\nLoadModule ssl_module modules/mod_ssl.so\n")
        httpd_conf_file.write("LoadModule socache_shmcb_module modules/mod_socache_shmcb.so\n")

    # Restart Apache to apply changes
    run_command("apachectl restart")

if __name__ == "__main__":
    configure_ssl_on_apache()
