import yt_dlp
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from threading import Thread
import subprocess
import os


def directory_change(): #directory change method
    new_directory = new_dir.get()
    with open('save_directory.txt', "w") as directory_file:
        directory_file.write(new_directory)
    directory_file.close()
    messagebox.showinfo(title = "directory changed!", message=f"changed the save directory to:\n{new_directory}") #showing message
    return f"directory changed to {new_directory}"

def dir_not_found_change():
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
        messagebox.showerror(title= "directory not found! Please change the directory or create a save_directory.txt file")



# creating ffmpeg install thread
def ffmpeg_install_threading():
    ffmpeg_thread = Thread(target=ffmpeg_install)
    ffmpeg_thread.start()

# ffmpeg install
def ffmpeg_install():
    ...
    #not yet implemented.
    #setup.py file does work to an extent though




 # using multithreading because otherwise tkinter would freeze for as long as there's another task on the same thread running.
 # apparently it likes the thread it uses to just be its own private thread
def single_video_threading():
    single_video_thread = Thread(target=single_video_download)
    single_video_thread.start()

def playlist_threading():
    playlist_thread = Thread(target=playlist_dowload)
    playlist_thread.start()



#single video downloads
def single_video_download(): #single video download method
    link = url.get() #getting the video url from the entry box
    try:
        with yt_dlp.YoutubeDL() as ydl:
            info_dict = ydl.extract_info(f'{link}', download=False)
            video_title = info_dict.get('title', None)

        directory = read_directory()[0]  # getting the save directory

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

        print(f"downloading {video_title}") #status updates
        download_status.config(text=f"downloading {video_title}...")
        download_status.update()
        print(link)

        resolution = clicked.get() #getting the resolution
        print(resolution)

        subtitles = False #subtitles are off by default so this is also off by default
        subtitle_option = sub_clicked.get() #getting subtitle choice
        print(subtitle_option) #printing it for debug purposes
        if subtitle_option == "yes":
            subtitles = True

        audio_only = False #audio only download is off by default
        audio_only_option = audio_only_choice.get() #getting the dropdown menu choice (no by default)
        if audio_only_option == "yes":
            audio_only = True

        if not audio_only:
            #setting yt-dlp options
            ydl_options = {
                'format': f'bestvideo[height<={resolution}][ext=mp4]+bestaudio[ext=m4a]/mp4', #video with a resolution of at least 1080p
                'subtitlesformat': 'vtt', # Specify the subtitles format
                'writeautomaticsub': subtitles, # Download auto-generated subtitles
                'writesubtitles': subtitles, # Download subtitles
                'outtmpl': f'{directory}\\{video_title} - {resolution}p.mp4', #output folder and name
                'merge_output_format': 'mp4', #the key name speaks for itself
                'postprocessors': [{'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'}] #it does require ffmpeg to work.
            }
        else:
            quality = quality_choice.get()
            print(quality)
            ydl_options = {
                    'format': 'bestaudio/best',
                    'outtmpl': f'{directory}\\{video_title} - {quality}kbps',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': f'{quality}'
                    }]
                }

        with yt_dlp.YoutubeDL(ydl_options) as ydl:
            ydl.download([f'{link}']) #downloading the video

        print(f"downloaded {video_title} successfully")
        download_status.config(text=f'downloaded {video_title} successfully')
        download_status.update()
    except:
        print("error while downloading the video")
        download_status.config(text= "failed to download the video")
        download_status.update()


#playlist downloads
def playlist_dowload():
    playlist_link = playlist_url.get() #getting playlist url
    directory = read_directory()[0]  # getting the save directory


    with yt_dlp.YoutubeDL() as ydl:
        print("extracting playlist info...")
        playlist_info = ydl.extract_info(playlist_link, download=False) #getting the playlist info
        number_of_vids = len(playlist_info['entries']) #getting the number of videos
        downloaded_videos = 0  # counter for downloaded videos
        total_percentage = 0  # download percentage
        percent_per_vid = (1 / number_of_vids) * 100  # percentage per single video download
        failed_downloads = 0  # planning on adding this to the UI as well in the future so I guess it's a TODO


        for video in playlist_info['entries']:


            link = video["webpage_url"] # getting the video url
            print(link)
            info_dict = ydl.extract_info(link, download=False)
            video_title = info_dict['title'] #getting the title (you could also get many more things)
            progressbar.start()
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

            try:  # huge try except for all of this just in case heart
                # replacing all "problematic" characters
                print("checking if the title is valid...")
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
                #status update
                current_video.config(text=f"Downloading {video_title}...")


                resolution = clicked.get()  # getting the resolution
                print(resolution)

                subtitles = False
                subtitle_option = sub_clicked.get()
                print(subtitle_option)
                if subtitle_option == "yes":
                    subtitles = True

                audio_only = False  # audio only download is off by default
                audio_only_option = audio_only_choice.get()  # getting the dropdown menu choice (no by default)
                if audio_only_option == "yes":
                    audio_only = True

                if not audio_only:
                    # setting yt-dlp options
                    ydl_options = {
                        'format': f'bestvideo[height<={resolution}][ext=mp4]+bestaudio[ext=m4a]/mp4',
                        # video with a resolution of at least 1080p
                        'subtitlesformat': 'vtt',  # Specify the subtitles format
                        'writeautomaticsub': subtitles,  # Download auto-generated subtitles
                        'writesubtitles': subtitles,  # Download subtitles
                        'outtmpl': f'{directory}\\{video_title} - {resolution}p.mp4',  # output folder and name
                        'merge_output_format': 'mp4',  # the key name speaks for itself
                        'postprocessors': [{'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'}]
                        # it does require ffmpeg to work.
                    }
                else:
                    quality = quality_choice.get()
                    print(quality)
                    ydl_options = {
                            'format': 'bestaudio/best',
                            'outtmpl': f'{directory}\\{video_title} - {quality}kbps',
                            'postprocessors': [{
                                'key': 'FFmpegExtractAudio',
                                'preferredcodec': 'mp3',
                                'preferredquality': f'{quality}'
                            }]
                        }

                # Downloading the video
                with yt_dlp.YoutubeDL(ydl_options) as ydl:
                    ydl.download([f'{link}'])


                current_video.config(text=f"downloaded {video_title} successfully!")
                print(f"downloaded {video_title} successfully!")
                current_video.update()
                downloaded_videos += 1 #updating the taskbar
                progressbar.update_idletasks()
                total_percentage += percent_per_vid
                progress_percent.config(text=f'{total_percentage:.2f}%')
                downloaded.config(text=f'{downloaded_videos}/{number_of_vids} downloaded')
                downloaded.update() #updating downloaded counter on gui
                progress_percent.update() #updating progress percent (pp) on the gui
                if downloaded_videos == number_of_vids:
                    progressbar.stop() # resetting and stopping the progressbar


            except: #some error occured during this entire proccess
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
if "yt_icon.ico" in os.listdir(os.getcwd()):
    root.iconphoto(False, PhotoImage(file= f"yt_icon.ico")) #changing the icon of the window to that of
Label(root, text="Youtube Downloader",bg='#0F0F0F',fg='#fafafa' , font='italic 15 bold').pack(pady=10) #first title label

#Downloadng a single video
Label(root, text = "Download a single video: ",bg='#0F0F0F',fg='#fafafa', font="italic 10").place(x=37, y=72) #label
url = Entry(root, width=60) #creating entry box
url.place(x=185, y=72) #fixed position (would look worse the higher the resolution of the monitor gets)
Button(root, text="Download",bg='#267cc7', command=single_video_threading).place(x=555, y=67) #creating the button using random color as background color
download_status = Label(root, text="", bg='#0f0f0f', fg="#fafafa", font='italic 10')
download_status.place(x=185, y=92) #decided to also add download status for single video downloads

# resolutions drop menu
resolution_options = [
    "144",
    "240",
    "360",
    "480",
    "720",
    "1080",
    "1440",
    "2160",
    "4320"
]

quality_options = [
    "128",
    "192",
    '256'
]
quality_choice = StringVar()
quality_choice.set('128')
quality_drop = OptionMenu(root, quality_choice, *quality_options)
quality_drop.config(bg='#0F0F0F', fg='#fafafa', font="italic 10")
quality_drop.place(x=865, y=140)

clicked = StringVar()
clicked.set("1080")
drop = OptionMenu(root, clicked, *resolution_options)
drop.place(x=625, y=65)
drop.config(bg='#0F0F0F', fg='#fafafa', font="italic 10")

#yes or no for subtitles
Label(root, text = "Do you want to also download subtitle file?", bg='#0F0F0F',fg='#fafafa', font="italic 10", ).place(x=700, y=35)
sub_options = ["yes", "no"]
sub_clicked = StringVar()
sub_clicked.set("no")
sub_drop = OptionMenu(root, sub_clicked, *sub_options)
sub_drop.place(x=800, y=65)
sub_drop.config(bg='#0F0F0F', fg='#fafafa', font="italic 10")

# yes or no for audio only download
audio_only_choices = ['yes', 'no']
audio_only_choice = StringVar()
audio_only_choice.set("no")
audio_only_drop = OptionMenu(root, audio_only_choice, *audio_only_choices)

Label(root, text= "Do you want to download audio only?", bg="#0f0f0f", fg="#fafafa", font="italic 10").place(x=710, y=110)
audio_only_drop.place(x=800, y=140)
audio_only_drop.config(bg='#0F0F0F', fg='#fafafa', font="italic 10")

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
# Button(root, text="install ffmpeg",bg='#267cc7', command=ffmpeg_install_threading).place(x=600, y= 350)


Button(root, text = "QUIT", width=10, height=1, bg='RED', fg='#fafafa', command=root.destroy).place(relx= .9, rely=.9, anchor=CENTER)
root.mainloop() #executing tkinter object
