from pytube import YouTube
from pytube import Playlist
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import os

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



def single_video_download(): #single video download method
    link = url.get() #getting the video url from the entry box
    youtube_object = YouTube(link) #creating youtube object
    try:
        video_title = youtube_object.title
    except:
        video_title = "not available"
    print(f"downloading {video_title}")
    download_status.config(text=f"downloading {video_title}...")
    download_status.update()
    youtube_object1080 = youtube_object.streams.get_by_itag(37) #getting highest resolution
    try:
        directory = read_directory()[0]
        youtube_object1080.download(directory)
        print(f"{video_title} downloaded successfully\n")
        download_status.config(text=f"downloaded {video_title} successfully!")
        download_status.update()
    except:
        try:
            youtube_object = youtube_object.streams.get_highest_resolution()
            youtube_object.download(directory)
            print(f"{video_title} downloaded successfully\n")
            download_status.config(text=f"downloaded {video_title} successfully!")
            download_status.update()
        except:
            print("there was an error while downloading the video")
            download_status.config(text=f"there was an error while downloading {video_title}")
            download_status.update()

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
            video_title = "n/a" #the file is still going to be saved as the original title as this is just for the gui and prints

        current_video.config(text=f'Currently downloading: {video_title}', bg='#0F0F0F', fg='#fafafa') #displaying currently downloading video
        current_video.update() #updating the gui

        print(f"Downloading {video_title}...") #a print for debugging

        if f"{video_title}.mp4" in os.listdir(read_directory()[0]): #seeing if the video has already been downloaded
            print("file already downloaded\n")
            progressbar.step(percent_per_vid)
            downloaded_videos += 1
            total_percentage += percent_per_vid
            progress_percent.config(text=f'{total_percentage:.2f}%')
            downloaded.config(text=f'{downloaded_videos}/{number_of_vids} downloaded')
            downloaded.update() #updating downloaded counter on gui
            progress_percent.update() #updating progress percent (pp) on the gui
            if downloaded_videos == number_of_vids:
                progressbar.stop() # resetting and stopping the progressbar
            continue

        try: #huge try except for all of this just in case heart
            vid_link = video.watch_url
            youtube_object = YouTube(vid_link)
            youtube_object1080 = youtube_object.streams.get_by_itag(37) #itag 37 = 1080p video - getting the stream and downloading it

            try: #trying to download it at 1080p
                directory = read_directory()[0] #getting the save directory
                youtube_object1080.download(directory) # downloading the video
                print(f"{video_title} downloaded successfully\n")
                current_video.config(text=f"{video_title} downloaded successfully", bg='#0F0F0F', fg='#fafafa')
            except: #if it fails to download it we try to download the highest resolution it can download
                try: #trying to download the highest resolution
                    youtube_object = youtube_object.streams.get_highest_resolution()
                    youtube_object.download(directory) #downloading video
                    print(f"{video_title} downloaded successfully\n")
                    current_video.config(text=f"{video_title} downloaded successfully", bg='#0F0F0F', fg='#fafafa')
                except: #there's some other error preventing it from downloading
                    print("there was an error while downloading the video")
                    current_video.config(text=f"there was an error while downloading the video", bg='#0F0F0F', fg='#fafafa')

            downloaded_videos += 1 #updating the taskbar
            progressbar.step(percent_per_vid)
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
Button(root, text="Download",bg='#267cc7', command=single_video_download).place(x=555, y=67) #creating the button using random color as background color
download_status = Label(root, text="", bg='#0f0f0f', fg="#fafafa", font='italic 10')
download_status.place(x=185, y=92) #decided to also add download status for single video downloads


#Downloading a playlist
Label(root, text = "Download a playlist: ",bg='#0F0F0F',fg='#fafafa', font="italic 10").place(x=37, y=150)
playlist_url = Entry(root, width=60)
playlist_url.place(x=185, y=150)
Button(root, text="Download", bg='#267cc7', command=playlist_dowload).place(x = 555, y = 145)
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