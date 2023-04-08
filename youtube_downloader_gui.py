from pytube import YouTube
from pytube import Playlist
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from time import sleep
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
    youtube_object = youtube_object.streams.get_highest_resolution() #getting highest resolution
    try:
        directory = read_directory()[0]
        youtube_object.download(directory)
    except:
        print("there was an error while downloading the video")
    print(f"{youtube_object.title} downloaded successfully\n")

def playlist_dowload():
    playlist_link = playlist_url.get()
    playlist = Playlist(playlist_link)
    for video in playlist.videos:
        current_video.config(text=f'Currently downloading: {video.title}', bg='#0F0F0F', fg='#fafafa')
        sleep(1)
        current_video.update()
        print(f"Downloading {video.title}...")
        try:
            vid_link = video.watch_url
            youtube_object = YouTube(vid_link)
            youtube_object = youtube_object.streams.get_highest_resolution()
            try:
                directory = read_directory()[0] #getting the save directory
                youtube_object.download(directory) # downloading the vide
            except:
                print("there was an error while downloading the video")
            print(f"{youtube_object.title} downloaded successfully\n")
            current_video.config(text = f"{youtube_object.title} downloaded successfully", bg='#0F0F0F', fg='#fafafa')
        except:
            print(f"failed to download video {video.title}")
            sleep(0.1)
            current_video.config(text=f'failed to download video "{video.title}"',bg='#0F0F0F', fg='#fafafa')
        sleep(1)
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

#Downloading a playlist
Label(root, text = "Download a playlist: ",bg='#0F0F0F',fg='#fafafa', font="italic 10").place(x=37, y=150)
playlist_url = Entry(root, width=60)
playlist_url.place(x=185, y=150)
Button(root, text="Download", bg='#267cc7', command=playlist_dowload).place(x = 555, y = 145)
current_video = Label(root, text='',bg='#0F0F0F') # not quite sure if I should delete that
current_video.place(x=185, y=170)

#adding the option to change a directory
Label(root, text="Change or add directory",bg='#0F0F0F', fg='#fafafa' ,font='italic 10').place(x=475, y= 300)
new_dir = Entry(root, width=48)
new_dir.place(x=400, y=325)
Button(root, text="Change dir",bg='#267cc7', command=directory_change).place(x=500, y= 350)

Button(root, text = "QUIT", width=10, height=1, bg='RED', fg='#fafafa', command=root.destroy).place(relx= .9, rely=.9, anchor=CENTER)
root.mainloop() #executing tkinter object