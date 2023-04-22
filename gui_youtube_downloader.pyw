from pytube import YouTube
from pytube import Playlist
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from threading import Thread
import subprocess
import os

ffmpeg = "ffmpeg"

def directory_change(): #directory change method
    new_directory = new_dir.get()
    with open('save_directory.txt', "w") as directory_file:
        directory_file.write(new_directory)
    directory_file.close()
    messagebox.showinfo(title = "directory changed!", message=f"changed the save directory to:\n{new_directory}") #showing message
    return f"directory changed to {new_directory}"


def read_directory(): #reading the contents of the save_directory file
    files = os.listdir()
    present = False
    for file in files: #Checking if the save directory file exists in the same directory as the script file.
        if file.startswith("save_directory"):
            present = True
    if present:
        with open("save_directory.txt", "r") as directory_file:
            directory = directory_file.readlines()
            directory_file.close()
            return directory
    else:
        messagebox.showerror(title="Error", message="Save file not found!\nPlease add a direcotry with change dir option") #showing an error
        win = Tk() #not really tested but it's supposed to be just a directory changer window.
        win.frame()
        win.geometry('325x125')
        Label(win, text="The file is missing!").place(x=100, y=10)
        Label(win, text="Change or add directory", font='italic 10').place(x=90, y=25)
        new_dir = Entry(win, width=48)
        new_dir.place(x=10, y=50)
        Button(win, text="Change dir", command=directory_change).place(x=120, y=75)
        win.mainloop()



 # using multithreading because otherwise tkinter would freeze for as long as there's another task on the same thread running.
 # apparently it likes the thread it uses to just be its own private thread
def single_video_threading():
    single_video_thread = Thread(target=single_video_download)
    single_video_thread.start()

def playlist_threading():
    playlist_thread = Thread(target=playlist_dowload)
    playlist_thread.start()



def merging(video_path, audio_path, video_title, output_path, download_type): #merging the video and audio files and deleting them after creating a new merged file - download type is to know from which function merging got called.
    if download_type == "single":
        download_status.config(text="Merging the 1080p audio and video files...") #status update
        download_status.update()
    else:
        current_video.config(text="Merging the 1080p audio and video files...")
        current_video.update()

    print("merging the audio and video file")
    try:
        cmd = f'{ffmpeg} -y -i "{video_path}" -i "{audio_path}" -c:v copy -c:a aac -strict experimental "{output_path}"' #cmd command
        subprocess.call(cmd, shell=True) #executing said command
        print("merged the video and audio file successfully") #status updates
        if download_type == "single":
            download_status.config(text=f"Merged the video and audio files successfully!") # status updates
            download_status.update()
        else:
            current_video.config(text="Merged the video and audio files successfully!")
            current_video.update()

    except: #there was some error that occured during the merge
        print("an error has occured during the merge") #status update
        if download_type == "single":
            download_status.config(text="An error has occured during the merge!") # status updates
            download_status.update()
        else:
            current_video.config(text="An error has occured during the merge!")
            current_video.update()

    print("deleting seperate audio and video files...")
    try:
        os.remove(video_path) #removing the vide and audio files
        os.remove(audio_path)
        print("deleted the seperate files successfully!\n")
    except:
        print("Couldn't delete the original files\n")


def download_720p_video(link):
    youtube_object = YouTube(link) #creating youtube object
    try:
        video_title = youtube_object.title #getting the title and because sometimes it just gives me an error when trying to get the title I will be catching such situations here
    except:
        try:
            youtube_object = YouTube(link) #retrying
            print(f"{youtube_object.title}, {youtube_object.streams}")
            video_title = youtube_object.title
        except:
            video_title = "not available" #default for when there's no title.

    if True: #just realized what this is doing but it's 4 am and I am not willing to think about it... I think I wanted to add a bool somewhere around here...
        directory = read_directory()[0]
        youtube_object = youtube_object.streams.get_highest_resolution()  # getting the highest resolution it can get
        res = youtube_object.resolution  # resolution for said video
        youtube_object.download(directory)  # downloading it
        # status updates
        print(
            f"{video_title} downloaded successfully at {res} resolution and {youtube_object.fps}fps {youtube_object.video_codec} codec  {youtube_object.bitrate} bitrate {youtube_object.filesize_mb} mb size\n")
        download_status.config(
            text=f"downloaded {video_title} successfully at {res} resolution and {youtube_object.fps}fps! ({youtube_object.filesize_mb:.2f} mb size)")
        download_status.update()
    else:
        download_status.config(text=f"error while downloading {video_title}...")
        download_status.update()
        print(f"error while downloading {video_title}")



#single video downloads
def single_video_download(): #single video download method
    link = url.get() #getting the video url from the entry box
    youtube_object = YouTube(link) #creating youtube object
    try:
        video_title = youtube_object.title #getting the title and because sometimes it just gives me an error when trying to get the title I will be catching such situations here
    except:
        try:
            youtube_object = YouTube(link) #retrying
            video_title = youtube_object.title
        except:
            video_title = "not available" #default for when there's no title.


    print(f"downloading {video_title}") #status updates
    download_status.config(text=f"downloading {video_title}...")
    download_status.update()


    #checking if ffmpeg is installed or not
    try:
        result = subprocess.run([f'{ffmpeg}', '--help'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        ffmpeg_installed = True
    except FileNotFoundError:
        ffmpeg_installed = False
    except subprocess.CalledProcessError:
        print("ffmpeg has not been installed correctly")

    if not ffmpeg_installed:
        print("ffmpeg is not installed. Lower resolution video will be installed instead...")
        download_720p_video(link=link) #downloading a 720p video instead of 1080p



    else:

        print(link)
        try:
            #trying to get 4k stream
            youtube_object_high_res = youtube_object.streams.filter(file_extension='mp4', res='2160p', only_video=True).first()#getting 2160p video resolution
        except:
            youtube_object_high_res = None

        if youtube_object_high_res is None: #1440p
            print("failed to get 4k stream... trying 1440p") #this can be caused by the video not having 4k to begin with or... well youtube being weird and pytube being inconsistent
            try:
                youtube_object = YouTube(link)
                youtube_object_high_res = youtube_object.streams.filter(file_extension="mp4", res='1440p', only_video=True).first()
            except:
                print("couldn't get 1440p")
                youtube_object_high_res = None

            if youtube_object_high_res is None: #1080p
                print("failed to get 1440p stream... trying 1080p") #same as 4k
                try:
                    youtube_object = YouTube(link)
                    youtube_object_high_res = youtube_object.streams.filter(file_extension="mp4", res='1080p', only_video=True).first() #no real way to notify someone if the file is being downloaded
                except:
                    try:
                        print("Couldn't get stream. Trying again...")
                        youtube_object = YouTube(link)
                        youtube_object_high_res = youtube_object.streams.filter(file_extension="mp4", res='1080p',
                                                                            only_video=True).first()  # no real way to notify someone if the file is being downloaded
                    except:
                        print("couldn't get 1080p video")
                        download_720p_video(link=link)

            else:
                print("got 1440p stream")
        else:
            print("got 4k stream")

        print("got higher resolution. Downloading audio...")
        youtube_object_audio = youtube_object.streams.filter(file_extension='mp4', only_audio=True).first() #getting the audio for said vide
        print("got audio stream")

        try:
            directory = read_directory()[0] #getting the save directory

            #replacing all "problematic" characters
            if "." in video_title:
                video_title = video_title.replace(".", "")
            elif "|" in video_title:
                video_title = video_title.replace("|", "")
            elif "\"" in video_title:
                video_title = video_title.replace("\"", "")
            elif "?" in video_title:
                video_title = video_title.replace("?", "")
            elif ":" in video_title:
                video_title = video_title.replace(":", "")
            elif "/" in video_title:
                video_title = video_title.replace("/", "")
            elif "\\" in video_title:
                video_title = video_title.replace("\\", "")
            elif "<" in video_title:
                video_title = video_title.replace("<", "")
            elif ">" in video_title:
                video_title = video_title.replace(">", "")
            elif "*" in video_title:
                video_title = video_title.replace("*", "")

            #downloading the audio and video streams
            print("downloading the audio and video streams...")
            print("downloading the video...")
            youtube_object_high_res.download(output_path=directory, filename=f"{video_title}.mp4") #downloading the high res video
            print(f"downloaded {video_title} at {youtube_object_high_res.resolution}")
            youtube_object_audio.download(output_path=directory, filename=f'{video_title}.mp3') #downloading the audio file

            print(f"{video_title} downloaded successfully at {youtube_object_high_res.resolution}\n") #status updates
            download_status.config(text=f"downloaded {video_title} successfully at {youtube_object_high_res.resolution} resolution!")
            download_status.update()
            merging(video_path=f'{directory}\\{video_title}.mp4', audio_path=f'{directory}\\{video_title}.mp3', video_title=video_title, output_path=f"{directory}\\{video_title} - {youtube_object_high_res.resolution}.mp4", download_type="single") #calling the merging function

        except:
            print("failed to download at high resolution so trying with the highest possible resolution (usually 720p)...") #failed to download 1080p meaning there was some error or the video doesn't have 1080p
            try:
                try:
                    os.remove(f'{directory}\\{video_title}.mp3')
                except:
                    print("no audio file to be deleted")
                youtube_object = youtube_object.streams.get_highest_resolution() #getting the highest resolution it can get
                res = youtube_object.resolution # resolution for said video
                youtube_object.download(directory) #downloading it
                #status updates
                print(f"{video_title} downloaded successfully at {res} resolution and {youtube_object.fps}fps {youtube_object.video_codec} codec  {youtube_object.bitrate} bitrate {youtube_object.filesize_mb} mb size\n")
                download_status.config(text=f"downloaded {video_title} successfully at {res} resolution and {youtube_object.fps}fps! ({youtube_object.filesize_mb:.2f} mb size)")
                download_status.update()
            except:
                print("there was an error while downloading the video") # some other error occured
                download_status.config(text=f"there was an error while downloading {video_title}") #status updates
                download_status.update()





#playlist downloads
def playlist_dowload():
    playlist_link = playlist_url.get()
    playlist = Playlist(playlist_link)
    number_of_vids = len(playlist.videos)
    progressbar.start()
    downloaded_videos = 0 #counter for downloaded videos
    total_percentage = 0 #download percentage
    percent_per_vid = (1/number_of_vids) * 100
    for video in playlist.videos:
        try: #I found that for some videos it inexplicably gives me an exception stating that it can't get the title of a video so I'm trying to catch it here.
            video_title = video.title
        except:
            print("error while getting the title of the video")
            video_title = "not available" #the file is still going to be saved as the original title as this is just for the gui and prints

        current_video.config(text=f'Currently downloading: {video_title}', bg='#0F0F0F', fg='#fafafa') #displaying currently downloading video
        current_video.update() #updating the gui

        print(f"Downloading {video_title}...")

        if f"{video_title}.mp4" in os.listdir(read_directory()[0]): #seeing if the video has already been downloaded
            print("file already downloaded\n")
            current_video.config(text=f"{video_title} already downloaded")
            downloaded_videos += 1
            total_percentage += percent_per_vid
            progress_percent.config(text=f'{total_percentage:.2f}%')
            downloaded.config(text=f'{downloaded_videos}/{number_of_vids} downloaded')
            downloaded.update() #updating downloaded counter on gui
            progress_percent.update() #updating progress percent (pp) on the gui
            progressbar.update_idletasks()
            if downloaded_videos == number_of_vids:
                progressbar.stop() # resetting and stopping the progressbar
            continue



        # checking if ffmpeg is installed or not
        try:
            result = subprocess.run([f'{ffmpeg}', '--help'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            ffmpeg_installed = True
        except FileNotFoundError:
            ffmpeg_installed = False
        except subprocess.CalledProcessError:
            print("ffmpeg has not been installed correctly")

        if not ffmpeg_installed:
            print("ffmpeg is not installed. Lower resolution video will be installed instead...")
            download_720p_video(link=video.watch_url)  # downloading a 720p video instead of 1080p
            current_video.config(text=f"{video_title} will be downloaded at lower resolutions due to the lack of ffmpeg")
            downloaded_videos += 1
            total_percentage += percent_per_vid
            progress_percent.config(text=f'{total_percentage:.2f}%')
            downloaded.config(text=f'{downloaded_videos}/{number_of_vids} downloaded')
            downloaded.update() #updating downloaded counter on gui
            progress_percent.update() #updating progress percent (pp) on the gui
            progressbar.update_idletasks()
            continue



        else:

            try:  # huge try except for all of this just in case heart
                vid_link = video.watch_url
                youtube_object = YouTube(
                    vid_link)  # same procedure as the single video downloads except it's for playlists

                # downloading it at 1080p
                youtube_object_high_res = youtube_object.streams.filter(file_extension='mp4', res='2160p',
                                                                        only_video=True).first()  # getting 1440p video resolution
                if youtube_object_high_res is None:
                    print("failed to get 4k stream... trying 1440p")
                    youtube_object_high_res = youtube_object.streams.filter(file_extension="mp4", res='1440p',
                                                                            only_video=True).first()
                    if youtube_object_high_res is None:
                        print("failed to get 1440p stream... trying 1080p")
                        youtube_object_high_res = youtube_object.streams.filter(file_extension="mp4", res='1080p',
                                                                                only_video=True).first()
                    else:
                        print("got 1440p stream")
                else:
                    print("got 4k stream")
                youtube_object_audio = youtube_object.streams.filter(file_extension='mp4',
                                                                     only_audio=True).first()  # getting the audio for said video

                try:

                    # replacing all "problematic" characters
                    if "." in video_title:
                        video_title = video_title.replace(".", "")
                    elif "|" in video_title:
                        video_title = video_title.replace("|", "")
                    elif "\"" in video_title:
                        video_title = video_title.replace("\"", "")
                    elif "?" in video_title:
                        video_title = video_title.replace("?", "")
                    elif ":" in video_title:
                        video_title = video_title.replace(":", "")
                    elif "/" in video_title:
                        video_title = video_title.replace("/", "")
                    elif "\\" in video_title:
                        video_title = video_title.replace("\\", "")
                    elif "<" in video_title:
                        video_title = video_title.replace("<", "")
                    elif ">" in video_title:
                        video_title = video_title.replace(">", "")
                    elif "*" in video_title:
                        video_title = video_title.replace("*", "")


                    current_video.config(text=f"Downloading {video_title}...")
                    directory = read_directory()[0]  # getting the save directory
                    print("checking if the title is valid...")
                    if "." in video_title: #This can cause issues if the title ends in ... as windows would just ignore and remove them but the title of the video still has it
                        video_title.replace(".", "")
                    print("downloading seperate streams...")
                    youtube_object_high_res.download(output_path=directory, filename=f'{video_title}.mp4')  # downloading the 1080p video
                    youtube_object_audio.download(output_path=directory,
                                                  filename=f'{video_title}.mp3')  # downloading the audio file
                    print(f"{video_title} downloaded successfully at {youtube_object_high_res.resolution}\n")  # status updates
                    current_video.config(text=f"downloaded {video_title} successfully at {youtube_object_high_res.resolution} resolution!")
                    current_video.update()
                    print("merging the audio and video files")
                    merging(video_path=f'{directory}\\{video_title}.mp4', audio_path=f'{directory}\\{video_title}.mp3',
                            video_title=video_title,
                            output_path=f"{directory}\\{video_title} - {youtube_object_high_res.resolution}p", download_type='playlist')  #calling the merging function

                except: #if it fails to download it we try to download the highest resolution it can download
                    print("failed to download high res version. trying to download with the highest possible resolution (usually 720p)")
                    try: #trying to download the highest resolution
                        youtube_object = youtube_object.streams.get_highest_resolution()
                        youtube_object.download(directory) #downloading video
                        print(f"{video_title} downloaded successfully at {youtube_object.resolution} resolution\n")
                        current_video.config(text=f"{video_title} downloaded successfully", bg='#0F0F0F', fg='#fafafa')
                    except: #there's some other error preventing it from downloading
                        print("there was an error while downloading the video")
                        current_video.config(text=f"there was an error while downloading the video", bg='#0F0F0F', fg='#fafafa')

                downloaded_videos += 1 #updating the taskbar
                progressbar.update_idletasks()
                total_percentage += percent_per_vid
                progress_percent.config(text=f'{total_percentage:.2f}%')
                downloaded.config(text=f'{downloaded_videos}/{number_of_vids} downloaded')
                downloaded.update() #updating downloaded counter on gui
                progress_percent.update() #updating progress percent (pp) on the gui
                if downloaded_videos == number_of_vids:
                    progressbar.stop() # resetting and stopping the progressbar

            except: #some other error occured during this entire proccess
                print(f"failed to download video {video_title}")
                current_video.config(text=f'failed to download video "{video_title}"',bg='#0F0F0F', fg='#fafafa')
                downloaded_videos += 1 #updating the taskbar
                progressbar.update_idletasks()
                total_percentage += percent_per_vid
                progress_percent.config(text=f'{total_percentage:.2f}%')
                downloaded.config(text=f'{downloaded_videos}/{number_of_vids} downloaded')
                downloaded.update() #updating downloaded counter on gui
                progress_percent.update() #updating progress percent (pp) on the gui
                if downloaded_videos == number_of_vids:
                    progressbar.stop() # resetting and stopping the progressbar

            current_video.update() #updating the window so it shows the download status


root = Tk() #creating tkinter object
root.frame() #creating the frame so it could be fullscreened
root.geometry('1053x450')#decided this is an optimal resolution
root.config(bg='#0F0F0F') #setting the background color to the youtube dark mode one
root.title("Youtube Downloader by jtw") #window title
root.iconphoto(False, PhotoImage(file= f"{os.getcwd()}\\yt_icon.ico")) #changing the icon of the window to that of youtube
Label(root, text="Youtube Downloader",bg='#0F0F0F',fg='#fafafa' , font='italic 15 bold').pack(pady=10) #first title label

#Downloadng a single video
Label(root, text = "Download a single video: ",bg='#0F0F0F',fg='#fafafa', font="italic 10").place(x=37, y=72) #label
url = Entry(root, width=60) #creating entry box
url.place(x=185, y=72) #fixed position (would look worse the higher the resolution of the monitor gets)
Button(root, text="Download",bg='#267cc7', command=single_video_threading).place(x=555, y=67) #creating the button using random color as background color
download_status = Label(root, text="", bg='#0f0f0f', fg="#fafafa", font='italic 10')
download_status.place(x=185, y=92) #decided to also add download status for single video downloads


#Downloading a playlist
Label(root, text = "Download a playlist: ",bg='#0F0F0F',fg='#fafafa', font="italic 10").place(x=37, y=150)
playlist_url = Entry(root, width=60)
playlist_url.place(x=185, y=150)
Button(root, text="Download", bg='#267cc7', command=playlist_threading).place(x = 555, y = 145)
current_video = Label(root, text='',bg='#0F0F0F', fg='#fafafa', font='italic 10') # not quite sure if I should delete that
current_video.place(x=185, y=170)

#creating a progressbar and everything related to it
progressbar = ttk.Progressbar(root, orient=HORIZONTAL, length=600, mode= 'determinate')
progressbar.pack(expand=True)
progressbar.place(x=150, y=235)
progress_percent = Label(root, text='', bg='#0f0f0f', fg='#fafafa', font='italic 10') #progress percent. pretty self explanatory
progress_percent.place(x=520, y=210)
downloaded = Label(root, text='', bg='#0f0f0f', fg='#fafafa', font='italic 10') #count for downloaded videos
downloaded.place(x=230, y=210)

#adding the option to change a directory
Label(root, text="Change or add directory",bg='#0F0F0F', fg='#fafafa' ,font='italic 10').place(x=475, y= 300)
new_dir = Entry(root, width=48)
new_dir.place(x=400, y=325)
Button(root, text="Change dir",bg='#267cc7', command=directory_change).place(x=500, y= 350)

Button(root, text = "QUIT", width=10, height=1, bg='RED', fg='#fafafa', command=root.destroy).place(relx= .9, rely=.9, anchor=CENTER)
root.mainloop() #executing tkinter object