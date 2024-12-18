#!/usr/bin/env python3

import os

# check if running under sudo 
if os.geteuid() != 0: 
    print('This script must be run with sudo.') 
    exit(1)

if os.path.dirname(os.path.abspath(__file__)) != os.getcwd():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

from connect_chaotic_aur import connect_chaotic_aur
from install_zenity import install_zenity
import subprocess


def install_recording_software():
    install_zenity()

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
            
            obs_result = os.system("pacman -Syu --noconfirm obs-studio")

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
    install_recording_software()