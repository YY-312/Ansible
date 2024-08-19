terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 2.16"
    }
  }
}

provider "docker" {
  host = "unix:///var/run/docker.sock"
}

resource "local_file" "firstlab_config" {
  content = <<EOF
name: firstlab

topology:
  nodes:
    csr-r1:
      kind: vr-csr
      image: vrnetlab/vr-csr:16.09.05
    apache-server:
      kind: linux
      image: httpd:latest
      binds:
        - ${path.module}/ssl:/usr/local/apache2/conf/ssl  # Mount SSL certs
      ports:
        - "80:80" # HTTP access
        - "443:443" # HTTPS ports
    linux-client:
      kind: linux
      image: dorowu/ubuntu-desktop-lxde-vnc:latest
      binds:
        - /dev/shm:/dev/shm
      ports:
        - "6080:80" # HTTP access
        - "5900:5900" # VNC access

  links:
    - endpoints: ["csr-r1:Gi2", "linux-client:eth1"]
    - endpoints: ["csr-r1:Gi3", "apache-server:eth1"]
EOF

  filename = "${path.module}/firstlab.clab.yml"
}

resource "null_resource" "deploy_containerlab" {
  provisioner "local-exec" {
    command = "sudo containerlab deploy --topo ${local_file.firstlab_config.filename} --reconfigure"
  }

  depends_on = [local_file.firstlab_config]
}
