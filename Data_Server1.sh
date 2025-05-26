#!/bin/bash

# Cek apakah perangkat /dev/sda1 ada
if lsblk /dev/sda1; then
    # Jika ada, mount ke /mnt/data
    mount /dev/sda1 /mnt/Data_Server1 || echo "Failed to mount /dev/sda1"
else
    echo "/dev/sda1 tidak ditemukan"
fi

