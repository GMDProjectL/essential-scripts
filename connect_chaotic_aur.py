#!/usr/bin/env python3

import os
import sys

if os.path.dirname(os.path.abspath(__file__)) != os.getcwd():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

# check if running under sudo 
if os.geteuid() != 0: 
    print('This script must be run with sudo.') 
    exit(1)


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


def connect_chaotic_aur():
    if check_for_chaotic_aur():
        print("Chaotic AUR already enabled")
        exit(0)
    
    enroll_chaotic_aur_keys(CHAOTIC_AUR_KEY)
    install_chaotic_aur_keyring()
    install_chaotic_aur_mirrorlist()
    update_system()

    print('Chaotic AUR successfully connected!')


if __name__ == "__main__":
    connect_chaotic_aur()