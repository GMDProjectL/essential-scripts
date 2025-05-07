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

from connect_chaotic_aur import connect_chaotic_aur
from install_zenity import install_zenity
import subprocess


def install_recording_software():
    install_zenity()

    admin_theme_fix = []

    if os.getenv("BUFF_UID") is not None:
        uid = int(os.getenv("BUFF_UID"))
        username = os.getenv("BUFF_USER")

        admin_theme_fix = [
            'pkexec', '--user', username,
            'env', f'XDG_RUNTIME_DIR=/run/user/{uid}'
        ] # WIP

    try:
        zenity_list_output = subprocess.check_output(
            [
                'zenity', '--list', '--text="Select your screen recording software"', '--checklist', '--multiple', '--column', '"Install?"', '--column', 'Software', '0', '"OBS"', '0', '"GPU Screen Recorder"'
            ]
        )
    except Exception as e:
        print(e)
        return

    if zenity_list_output.decode().strip() == '':
        print('No software selected.')
        return

    zenity_list = zenity_list_output.decode().strip().split('|')

    for software in zenity_list:
        if software == '"OBS"':
            print('Installing OBS...')
            
            obs_result = os.system("flatpak install -y flathub com.obsproject.Studio")

            if obs_result != 0:
                print('Failed to install OBS.')
                exit(obs_result)

        if software == '"GPU Screen Recorder"':
            print('Installing GPU Screen Recorder...')

            gsr_result = os.system("pacman -Syu --noconfirm gpu-screen-recorder-gtk")

            if gsr_result != 0:
                print('Failed to install GPU Screen Recorder.')
                exit(gsr_result)
    

if __name__ == "__main__":
    if '-h' in sys.argv or '--help' in sys.argv:
        print("Usage: sudo python3 install_recording_software.py\nSelects and installs screen recording software (OBS, GPU Screen Recorder). Requires root.")
        sys.exit(0)
    print("\033[92m[+] Starting screen recording software installation script...\033[0m")
    install_recording_software()
    print("\033[92m[+] Script complete.\033[0m")