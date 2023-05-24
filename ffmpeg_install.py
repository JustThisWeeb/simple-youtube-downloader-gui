import os
import requests
import subprocess

class Ffmpeg:
    def __init__(self):
        ...

    def download(self):
        print("downloading ffmpeg...")
        # url = 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-full.7z'
        url = 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip'
        response = requests.get(url)

        with open(f'{os.getcwd()}\\ffmpeg-release-essentials.zip', 'wb') as file:
            file.write(response.content)
        current_dir = os.listdir()
        if "ffmpeg-release-essentials.zip" in current_dir:
            print("downloaded ffmpeg!")
        else:
            print("ffmpeg has not been downloaded properly")

    def decompress(self):
        print("decompressing...")
        try:
            # subprocess.call(['7z', 'x', 'ffmpeg-release-full.7z'])
            subprocess.call(['7z', 'x', 'ffmpeg-release-essentials.zip'])
            print("decompressed succesfully")
        except:
            print("error during decompression.")

    def adding_ffmpeg_to_env_variables(self):
        print("adding ffmpeg to environment variables...")
        # os.environ["PATH"] += f"{os.getcwd()}\\ffmpeg-6.0-full_build.7z"
        try:
            # os.environ["PATH"] += f"{os.getcwd()}\\ffmpeg-6.0-full_build\\bin"
            os.environ["PATH"] += f"{os.getcwd()}\\ffmpeg-6.0-essentials_build\\bin"
            print('added ffmpeg to path. Testing to see if ffmpeg has been installed properly...\n')
        except:
            print("error while adding ffmpeg to path\n")
            return "error"

        try:
            result = subprocess.run([f'ffmpeg', '--help'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            ffmpeg_installed = True
            print("ffmpeg has been installed properly.\n")
        except FileNotFoundError:
            ffmpeg_installed = False
        except subprocess.CalledProcessError:
            print("ffmpeg has not been installed correctly. You might need to add it to path yourself... here's a wikihow guide - https://www.wikihow.com/Install-FFmpeg-on-Windows")
