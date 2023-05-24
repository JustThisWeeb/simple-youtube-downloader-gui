import subprocess
from winreg import *
import requests
import os
from ffmpeg_install import Ffmpeg
import platform
from time import sleep

#  Install the requests package using pip and capture the output
result = subprocess.run(['pip', 'install', 'yt-dlp'], capture_output=True)
#Print the output
print(result.stdout.decode('utf-8'))
if platform.system() == "Linux":
    package_manager = input("specify your package manager (eg apt, pacman etc.): ")
    result = subprocess.run(["sudo", package_manager, "ffmpeg"], capture_output=True)
    print(result.stdout.decode("utf-8"))
    sleep(5)
    quit()

while True:
    print("Select which option you'd like to use:")
    print('"1" - download ffmpeg\n'
          '"2" - decompress ffmpeg (requires ffmpeg to be installed and in the same folder as the script)\n'
          '"3" - add ffmpeg to environment variables in PATH (requires ffmpeg to be decompressed in the same folder as the script. Run 1 & 2 to do the steps before)'
          '\n"4" - quit the script\n\n')
    usr_in = input("your input: ")
    if usr_in == "1":
        Ffmpeg.download(Ffmpeg)
    elif usr_in == "2":
        Ffmpeg.decompress(Ffmpeg)
    elif usr_in == "3":
        Ffmpeg.adding_ffmpeg_to_env_variables(Ffmpeg)
    elif usr_in == "4":
        quit()
    else:
        print("incorrect input")






