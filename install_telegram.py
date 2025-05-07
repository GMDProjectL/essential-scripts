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


def install_telegram():
    result = os.system("pacman -S --noconfirm telegram-desktop")
    if result != 0:
        print("Failed to install telegram-desktop")
        exit(1)
    

if __name__ == "__main__":
    if '-h' in sys.argv or '--help' in sys.argv:
        print("Usage: sudo python3 install_telegram.py\nInstalls Telegram desktop client. Requires root.")
        sys.exit(0)
    print("\033[92m[+] Installing Telegram Desktop...\033[0m")
    install_telegram()
    print("\033[92m[+] Script complete.\033[0m")