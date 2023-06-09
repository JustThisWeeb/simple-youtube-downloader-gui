# Important
I will no longer update the pytube file as yt-dlp seems to have more features and is more stable (plus more recent). I have added the new features to the pytube file but am once again getting streamingdata error so I wouldn't be optimistic about it working again. The yt-dlp file will get my support in the future though. 



# Requirements: 
- now yt-dlp is required instead of pytube for the new file. 
- ffmpeg. The yt-dlp library uses ffmpeg to format the videos to mp4 so now it's actually a bigger requirement than in the old file that uses pytube. 


# Setup
You might notice the setup.py and ffmpeg_install.py files. You only need to run the setup.py file to install the libraries and ffmpeg. yt-dlp automatically starts installing the moment the script is run and then you'd be given 4 choices. 1 is to download ffmpeg, 2 to decompress (unzip) it, 3 is to add it to environment variables (This one actually doesn't work but I am working towards getting it to work) and 4 is to quit. 
I am also testing linux support and might update the files to be linux compatible in the near future (tomorrow)


# Funnily enough
Because yt-dlp is a fork of youtube-dl it can download videos from sites other than youtube. For example you can download videos from twitter, facebook, reddit etc. 
Here's the link to the list of supported sites - https://github.com/ytdl-org/youtube-dl/blob/master/docs/supportedsites.md 
=== Note that over half of them probably won't work. yt-dlp only fixed the youtube download option as far as I'm aware.

# simple-youtube-downloader-gui
As the same would suggest this is a simple youtube downloader with a gui. 
I essentially just reused the code from my other repository with the same name if you exclude the gui part.

now it's not really perfect but I did also make it in just a few hours while learning about tkinter. 

One note I'd like to make is that I actually replaced the original .py file with a .pyw file which only really prevents the command prompt from opening up.

At the end of every downloaded 1080p video you will see a "- 1080p" being added. This is mainly due to ffmpeg not liking when there are 2 files with the same name in the same folder but also to let you know that this is the 1080p video. - Now it will also say 2160p and 1440p depending on the resolution.

!!! One thing I would like to note is that while I have managed to download 4k and 1440p videos using this "updated" version it's somewhat random... For example I have not managed to download a single LTT video in 4k despite them having 4k yet was able to download 4k demos such as the one shown in the screenshot below. I have also managed to download 1440p demos in 1440p but as I said it's pretty random and doesn't always work. That said it does manage to download them in 1080p but still felt I should point that out.

![aaasdasdsa](https://user-images.githubusercontent.com/79314361/232321656-03fb504e-9f6c-4f6f-942a-d14c46003606.jpg)




if you do have ffmpeg installed and the videos get downloaded in lower resolutions then you could try the fix I've listed in the Possible issues part of this readme


# future plans 
- Fixing the progressbar (again)
- integrating the new features to the old file with pytube
- adding a setup file that automatically does just about everything setup related. I've already mostly done that but there's a slight issue related to adding ffmpeg to path. It can download it and if you have 7zip installed it can also decompress it. The only real issue is getting it added to path which doesn't really seem to work for some reason. I will add the file tomorrow and if it works it works and if it doesn't I will fix it later. 


# Requirements:
python 3.x
(python 3.11 download link - https://www.python.org/ftp/python/3.11.3/python-3.11.3-amd64.exe)

pytube - (in the command prompt) 
py -m pip install pytube

ffmpeg - 
64-bit: https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-full.7z

32-bit: https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-full-32bit-static.7z

1. Open the Start menu and search for "Environment Variables".
2. Click on "Edit the system environment variables".
3. Click on the "Environment Variables" button.
4. Under "System Variables", find the "Path" variable and click "Edit".
5. Click "New" and enter the path to the FFmpeg bin directory (e.g. "C:\ffmpeg\bin").
6. Click "OK" to close all the windows.


# Possible issues: 
1. Titles - while I have somewhat mitigated the issue there is just simply a bug with pytube. That means that sometimes the video titles won't be available. If that happens just try to download the video again until it works

2. ffmpeg not being recognized (You have installed it and tested in cmd and it works but videos are still only being downloaded at 720p) - open the .pyw file using some ide (You could use the IDLE ide which comes with python), go to line 9 and change 'ffmpeg' to the directory of your ffmpeg.exe file (e.g. C:\\Users\\User\\Downloads\\ffmpeg-6.0-full_build\\ffmpeg-6.0-full_build\\bin\\ffmpeg.exe) and make sure to make the backwards slashes double (C:\Users\User --> C:\\\Users\\\User) to avoid any possible issues with it. 

3. This is an issue with either pytube or just youtube's api (which is known to be somewhat weird) but while before there were issues with getting the video titles now there are also issues with getting the streaming data of a video. This means that before today's "fix" (didn't really fix it) it failed to get the higher resolution streams (note that even if a video doesn't have high resolution streams it still should be a None object and not give me a pytube key error). The "fix" I made didn't really so much fix it as it simply stopped it from giving you an error and actually trying to get all resolutions. If it doesn't manage to get even 1080p resolution it would simply download the highest resolution it can get. If you encounter such an issue I don't really have a fix other than telling you to try again until it either works or you get annoyed. I'd recommend not trying over 3 times and if you really need that video with higher resolution you could try restarting the script and trying 3 more times and if that doesn't work then the issue with youtube's streaming data has probably worsened and I can't really do much about that other than just reporting the issue to the pytube github repository 

4. It got a 1080p video stream but didn't download the video. This is probably an issue with how I do things. You see when downloading the video I use the video title as a file name which means that if a video has some more "special" characters that windows doesn't allow in file names it will give an error when downloading the high resolution video. Then as an exception is raised it would simply revert to the highest resolution it can get and download which would normally be 720p (both higher and lower resolutions are possible). I have somewhat fixed the issue via just replacing the most common special characters I see in youtube titles.

# dev log I guess?
22/4/23 - added multithreading and fixed the crashing issue

28/4/23 - Really big changes related to a pytube bug I've been following for a few days (since around the 25th)

07/5/23 - pytube got patched but I have already added a few QoL features to the new file that uses yt-dlp so I will try integrating them with pytube. I will keep updating both files.

24/05/23 - had free time so I decided to add the new features to the pytube file and fix a few small issues with the yt-dlp file. Also finally uploaded the setup and ffmpeg files (I have had them for about 2 weeks now but forgot to actually upload them here) 
