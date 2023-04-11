# simple-youtube-downloader-gui
As the same would suggest this is a simple youtube downloader with a gui. 
I essentially just reused the code from my other repository with the same name if you exclude the gui part.

now it's not really perfect but I did also make it in just a few hours while learning about tkinter. I had an issue with the window becoming unresponsive when downloading a playlist and if you actually spam it it will crash. Not sure if the issue will get replicated on your end. 
One note I'd like to make is that I actually replaced the original .py file with a .pyw file which only really prevents the command prompt from opening up.

# future plans 
- Fixing the progressbar (again)
- Making support for ffmpegless users (will probably do this one today)


# Requirements:
python 3.x
(python 3.11 download link - https://www.python.org/ftp/python/3.11.3/python-3.11.3-amd64.exe)

pytube - (in the command prompt) 
py -m pip install pytube

ffmpeg - 
64-bit: https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-full.7z
32-bit: https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-full-32bit-static.7z

![image](https://user-images.githubusercontent.com/79314361/231166270-f2409d55-3524-4db9-b056-a5d1872f3544.png)


# Possible errors: 
1. Titles - while I have somewhat mitigated the issue there is just simply a bug with pytube. That means that sometimes the video titles won't be available. If that happens just try to download the video again until it works

2. ffmpeg not being recognized - open the .pyw file using some ide (You could use the IDLE ide which comes with python), scroll to line 52 and change ffmpeg to the directory of your ffmpeg.exe file (e.g. C:\\Users\\User\\Downloads\\ffmpeg-6.0-full_build\\ffmpeg-6.0-full_build\\bin\\ffmpeg.exe) and make sure to make the backwards slashes double (C:\Users\User --> C:\\Users\\User) to avoid any possible issues with it


