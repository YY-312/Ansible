# Example Dockerfile
FROM ubuntu:latest

# Install QEMU and necessary tools
RUN apt-get update && apt-get install -y qemu-system-x86

# Copy your CSR1000V ISO into the container
COPY csr1000v-universalk9.16.09.05.iso /root/csr1000v.iso

# Set the working directory
WORKDIR /root

# Command to run QEMU with CSR1000V ISO
CMD ["qemu-system-x86_64", "-cdrom", "csr1000v.iso"]
