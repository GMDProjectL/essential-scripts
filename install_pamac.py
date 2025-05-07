#!/usr/bin/env python3

import os


import sys

# Relaunch as sudo/root if not already root
if os.geteuid() != 0:
    print("\033[93m[!] Not running as root. Re-executing with sudo...\033[0m")
    try:
        os.execvp("sudo", ["sudo", sys.executable] + sys.argv)
    except Exception as e:
        print(f"\033[91m[!] Could not escalate privileges: {e}\033[0m")
        sys.exit(1)

if os.path.dirname(os.path.abspath(__file__)) != os.getcwd():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

import sys
from connect_chaotic_aur import connect_chaotic_aur, update_system


def install_pamac():
    connect_chaotic_aur()

    print("Installing Pamac...")

    pamac_result = os.system("pacman -S --noconfirm pamac")

    if pamac_result != 0:
        print("Pamac installation failed.")
        sys.exit(pamac_result)


if __name__ == "__main__":
    if '-h' in sys.argv or '--help' in sys.argv:
        print("Usage: sudo python3 install_pamac.py\nInstalls Pamac package manager. Requires root.")
        sys.exit(0)
    print("\033[92m[+] Starting Pamac installation script...\033[0m")
    install_pamac()
    print("\033[92m[+] Pamac installation script completed.\033[0m")