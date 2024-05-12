# import os
# import requests
# import subprocess
#
# class Ffmpeg:
#     def __init__(self):
#         ...
#
#     def download(self):
#         print("downloading ffmpeg...")
#         # url = 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-full.7z'
#         url = 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip'
#         response = requests.get(url)
#
#         with open(f'{os.getcwd()}/ffmpeg-release-essentials.zip', 'wb') as file:
#             file.write(response.content)
#         current_dir = os.listdir()
#         if "ffmpeg-release-essentials.zip" in current_dir:
#             print("downloaded ffmpeg!")
#         else:
#             print("ffmpeg has not been downloaded properly")
#
#     def decompress(self):
#         print("decompressing...")
#         try:
#             # subprocess.call(['7z', 'x', 'ffmpeg-release-full.7z'])
#             subprocess.call(['7z', 'x', 'ffmpeg-release-essentials.zip'])
#             print("decompressed succesfully")
#         except:
#             print("error during decompression.")
#
#     def adding_ffmpeg_to_env_variables(self):
#         print("adding ffmpeg to environment variables...")
#         # os.environ["PATH"] += f"{os.getcwd()}\\ffmpeg-6.0-full_build.7z"
#         try:
#             # os.environ["PATH"] += f"{os.getcwd()}\\ffmpeg-6.0-full_build\\bin"
#             os.environ["PATH"] += f"{os.getcwd()}/ffmpeg-6.0-essentials_build/bin"
#             print('added ffmpeg to path. Testing to see if ffmpeg has been installed properly...\n')
#         except:
#             print("error while adding ffmpeg to path\n")
#             return "error"
#
#         try:
#             result = subprocess.run([f'ffmpeg', '--help'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
#             ffmpeg_installed = True
#             print("ffmpeg has been installed properly.\n")
#         except FileNotFoundError:
#             ffmpeg_installed = False
#         except subprocess.CalledProcessError:
#             print("ffmpeg has not been installed correctly. You might need to add it to path yourself... here's a wikihow guide - https://www.wikihow.com/Install-FFmpeg-on-Windows")
#
# import yt_dlp
# import datetime
# link = 'https://music.youtube.com/watch?v=LCDfmnzf-JA&feature=share'
#
# with yt_dlp.YoutubeDL() as ydl:
#     info_dict = ydl.extract_info(link, download=False)
#
#     title = info_dict.get('title', 'Unknown Title')
#     artist = info_dict.get('uploader', 'Unknown Artist')
#     thumbnail = info_dict.get('thumbnail', 'default.jpg')
#     album = info_dict.get('album', 'Unknown album')
#     genre = info_dict.get('genre', "Unknown genre")
#     date_uploaded = info_dict.get('upload_date', None)
#     length = info_dict.get('duration', 0)
#
#     # Format date_uploaded as datetime object
#     # date_uploaded = datetime.datetime.strptime(date_uploaded, "%Y%m%d") if date_uploaded else None
#
#     # Format length as minutes and seconds
#     length_minutes = length // 60
#     length_seconds = length % 60
#
#     # Print the extracted metadata
#     print('Title:', title)
#     print('Artist:', artist)
#     print('Album:', album)
#     print('Date of Creation (Upload):', date_uploaded[0:4])
#     print('Length:', f'{length_minutes}:{length_seconds:02d}')
#
# def download_thumbnail(img_link):
#     response = requests.get(img_link)
#     with open(f"K:/pictures/temporary_thumbnail.jpeg", 'wb') as f:
#         f.write(response.content)
#         f.close()
# download_thumbnail(thumbnail)


import os
import requests
import subprocess
from time import sleep

class Ffmpeg:
    def __init__(self):
        ...

    def download(self):

        print("downloading ffmpeg...")
        # url = 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-full.7z'
        url = 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip'

        # checking if ffmpeg has already been downloaded
        current_dir_list = os.listdir()
        for file in current_dir_list:
            if "ffmpeg-release" in file:
                print("Ffmpeg seems to have been downloaded. Skipping...")
                return 0

        # actual download
        response = requests.get(url)
        with open(f'{os.getcwd()}/ffmpeg-release-essentials.zip', 'wb') as file:
            file.write(response.content)
        current_dir = os.listdir()

        # just debug messages I guess.
        if "ffmpeg-release-essentials.zip" in current_dir:
            print("downloaded ffmpeg!")
        else:
            print("ffmpeg has not been downloaded properly")

    def decompress(self):
        current_dir_list = os.listdir()
        for file in current_dir_list:
            if "ffmpeg-7.0-essentials_build" in file:
                print("Ffmpeg seems to have been decompressed. Skipping...")
                return 0

        print("decompressing...")
        try:
            # subprocess.call(['7z', 'x', 'ffmpeg-release-full.7z'])
            subprocess.call(['7z', 'x', 'ffmpeg-release-essentials.zip'])
            print("decompressed succesfully!\nDeleting the original zip file...")
            os.remove("ffmpeg-release-essentials.zip")
            print("Deleted the original zip file.")

        except:
            print("error during decompression.")

    def adding_ffmpeg_to_env_variables(self):
        print("adding ffmpeg to environment variables...")
        # os.environ["PATH"] += f"{os.getcwd()}\\ffmpeg-7.0-full_build.7z"
        try:
            current_dir = os.listdir()
            for file in current_dir:
                if "ffmpeg-" in file:
                    ffmpeg = file
            if "ffmpeg" not in file:
                file = "ffmpeg-7.0-essentials_build"
            # os.environ["PATH"] += f"{os.getcwd()}\\ffmpeg-7.0-full_build\\bin"
            new_env = os.environ["Path"] + f";{os.getcwd()}/{file}/bin"
            exp = f'setx Path "{new_env}"'
            subprocess.Popen(exp, shell=True).wait()
            os.environ.update()
            print("ffmpeg should have been added to the environment variables. Restart your system or logout to see the changes. Want to restart now? ")
            user_in = input("[y/n]: ")
            if user_in == "y":
                print("restarting in 3 seconds.")
                sleep(3)
                print("restarting...")
                os.system("shutdown /r /t 0")
                print("restarted - this is a debug message")
            else:
                print("ok. Auto close in 10 seconds")
                sleep(10)
                exit()

        except:
            print("error while adding ffmpeg to path\n")
            return "error"



# basically check if the os is widows or linux. If it's linux it's literally a single command that needs sudo permissions.
def linux_download():
    ...


ffmpeg_var = Ffmpeg()
ffmpeg_var.download()
ffmpeg_var.decompress()
ffmpeg_var.adding_ffmpeg_to_env_variables()
