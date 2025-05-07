#!/usr/bin/env python3

import os
import sys

if os.path.dirname(os.path.abspath(__file__)) != os.getcwd():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

import sys

# Relaunch as sudo/root if not already root
if os.geteuid() != 0:
    print("\033[93m[!] Not running as root. Re-executing with sudo...\033[0m")
    try:
        os.execvp("sudo", ["sudo", sys.executable] + sys.argv)
    except Exception as e:
        print(f"\033[91m[!] Could not escalate privileges: {e}\033[0m")
        sys.exit(1)


CHAOTIC_AUR_KEY = '3056513887B78AEB'


def read_pacman_repos_file() -> str:
    with open('/etc/pacman.conf', "r") as f:
        return f.read()


def check_for_chaotic_aur():
    pacman_repos = read_pacman_repos_file()
    if '[chaotic-aur]' in pacman_repos:
        return True
    
    return False


def enroll_chaotic_aur_keys(chaotic_aur_key: str):
    recv_result = os.system(f'pacman-key --recv-key {chaotic_aur_key} --keyserver keyserver.ubuntu.com')

    if recv_result != 0:
        print(f"Failed to enroll Chaotic AUR recv-key: code {recv_result}", file=sys.stderr)
        exit(recv_result)

    lsign_result = os.system(f'pacman-key --lsign-key {chaotic_aur_key}')

    if lsign_result != 0:
        print(f"Failed to enroll Chaotic AUR lsign-key: code {lsign_result}", file=sys.stderr)
        exit(lsign_result)


def install_chaotic_aur_keyring():
    keyring_result = os.system("pacman -U --noconfirm 'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-keyring.pkg.tar.zst'")

    if keyring_result != 0:
        print(f"Failed to install Chaotic AUR keyring: code {keyring_result}", file=sys.stderr)
        exit(keyring_result)


def install_chaotic_aur_mirrorlist():
    mirrorlist_result = os.system("pacman -U --noconfirm 'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-mirrorlist.pkg.tar.zst'")

    if mirrorlist_result != 0:
        print(f"Failed to install Chaotic AUR mirrorlist: code {mirrorlist_result}", file=sys.stderr)
        exit(mirrorlist_result)


def update_system():
    update_result = os.system("sudo pacman --noconfirm -Syyuu")

    if update_result != 0:
        print(f"Failed to update system: code {update_result}", file=sys.stderr)
        exit(update_result)


def append_mirrorlist():
    with open('/etc/pacman.conf', 'a') as f:
        f.write('''
[chaotic-aur]
Include = /etc/pacman.d/chaotic-mirrorlist''')


def connect_chaotic_aur():
    if check_for_chaotic_aur():
        print("Chaotic AUR already enabled")
        return
    
    enroll_chaotic_aur_keys(CHAOTIC_AUR_KEY)
    install_chaotic_aur_keyring()
    install_chaotic_aur_mirrorlist()

    append_mirrorlist()

    update_system()

    print('Chaotic AUR successfully connected!')


if __name__ == "__main__":
    if '-h' in sys.argv or '--help' in sys.argv:
        print("Usage: sudo python3 connect_chaotic_aur.py\nAdds and sets up the Chaotic AUR repository. Requires root/sudo.")
        sys.exit(0)
    print("\033[92m[+] Connecting Chaotic AUR repository...\033[0m")
    connect_chaotic_aur()
    print("\033[92m[+] Script complete.\033[0m")