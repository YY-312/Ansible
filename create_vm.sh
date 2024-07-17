#!/bin/bash

# Variables
VM_NAME="csr1000v"
ISO_PATH="C:\Users\LaiYa\AppData\Local\Programs\OpenTofu\testing"
VBOX_DISK_PATH="$HOME/${VM_NAME}.vdi"

# Create VM
VBoxManage createvm --name "$VM_NAME" --ostype "Other_64" --register

# Modify VM settings
VBoxManage modifyvm "$VM_NAME" --memory 2048 --vram 16 --nic1 nat

# Create a virtual hard disk
VBoxManage createhd --filename "$VBOX_DISK_PATH" --size 8192

# Attach the virtual hard disk
VBoxManage storagectl "$VM_NAME" --name "SATA Controller" --add sata --controller IntelAhci
VBoxManage storageattach "$VM_NAME" --storagectl "SATA Controller" --port 0 --device 0 --type hdd --medium "$VBOX_DISK_PATH"

# Attach the ISO file
VBoxManage storagectl "$VM_NAME" --name "IDE Controller" --add ide
VBoxManage storageattach "$VM_NAME" --storagectl "IDE Controller" --port 1 --device 0 --type dvddrive --medium "$ISO_PATH"

# Output VM ID
echo "{\"vm_id\": \"$VM_NAME\"}"
