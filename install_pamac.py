#!/usr/bin/env python3

import os

# check if running under sudo 
if os.geteuid() != 0: 
    print('This script must be run with sudo.') 
    exit(1)

if os.path.dirname(os.path.abspath(__file__)) != os.getcwd():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

import sys
from connect_chaotic_aur import connect_chaotic_aur, update_system


connect_chaotic_aur()


def install_pamac():
    print("Installing Pamac...")

    update_system()
    connect_chaotic_aur()
    update_system()

    pamac_result = os.system("pacman -S --noconfirm pamac")

    if pamac_result != 0:
        print("Pamac installation failed.")
        sys.exit(pamac_result)


if __name__ == "__main__":
    install_pamac()