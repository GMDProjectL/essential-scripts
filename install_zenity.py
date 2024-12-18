#!/usr/bin/env python3

import os

# check if running under sudo 
if os.geteuid() != 0: 
    print('This script must be run with sudo.') 
    exit(1)

if os.path.dirname(os.path.abspath(__file__)) != os.getcwd():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))


def install_zenity():
    result = os.system("pacman -Syu --noconfirm zenity")
    if result != 0:
        print("Failed to install zenity")
        exit(1)
    

if __name__ == "__main__":
    install_zenity()