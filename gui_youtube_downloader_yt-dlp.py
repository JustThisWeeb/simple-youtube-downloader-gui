from mutagen.easyid3 import EasyID3
from mutagen.easymp4 import EasyMP4
import requests
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

def download_thumbnail(img_link, directory): #downloading the thumbnail file which will later be deleted.
    print("getting the response")
    response = requests.get(img_link)
    print('got the response')
    with open(f"{directory}/temporary_cover.jpeg", 'wb') as f:
        print('downloading response content')
        f.write(response.content)
        f.close()
        print("downloaded the thumbnail")

#single video downloads
def single_video_download(): #single video download method
    link = url.get() #getting the video url from the entry box
    try:
        with yt_dlp.YoutubeDL() as ydl:
            info_dict = ydl.extract_info(f'{link}', download=False)
            video_title = info_dict.get('title', None)
        metadata_chosen_option = metadata_choice.get()
        if metadata_chosen_option == "yes":
            with yt_dlp.YoutubeDL() as ydl:
                info_dict = ydl.extract_info(f'{link}', download=False)
                artist = info_dict.get('uploader', 'Unknown Artist')
                print(artist)
                thumbnail = info_dict.get('thumbnail', 'default.jpg')
                print(thumbnail)
                album = info_dict.get('album', 'Unknown album')
                print(album)
                genre = info_dict.get('genre', "Unknown genre")
                print(genre)
                date_uploaded = info_dict.get('upload_date', None)
                print(date_uploaded[0:4])
                length = info_dict.get('duration', 0)
                print(length)

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
                'outtmpl': f'{directory}/{video_title} - {resolution}p.mp4', #output folder and name
                'merge_output_format': 'mp4', #the key name speaks for itself
                'postprocessors': [{'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'}] #it does require ffmpeg to work.
            }
        else:
            quality = quality_choice.get()
            print(quality)
            ydl_options = {
                    'format': 'bestaudio/best',
                    'outtmpl': f'{directory}/{video_title} - {quality}kbps',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': f'{quality}'
                    }
                    ],
                'extractaudio': True,
                'audioformat': 'mp3',
                }

        with yt_dlp.YoutubeDL(ydl_options) as ydl:
            ydl.download([f'{link}']) #downloading the video

        #downloading the video metadata
        print("checking the metadata choices...")
        if metadata_chosen_option == "yes":
            print("adding metadata...")
            if audio_only:
                print("audio only metadata...")
                try:
                    print("specifying the directory of the file")
                    audio = EasyID3(f'{directory}/{video_title} - {quality}kbps.mp3')
                    print("title.")
                    audio['title'] = video_title
                    print("artist")
                    audio['artist'] = artist
                    print("album")
                    audio['album'] = album
                    print("date")
                    audio['date'] = date_uploaded[0:4]
                    print("length")
                    audio['length'] = str(length)
                    print("saving...")
                    print(audio.keys())
                    print(audio.values())
                    audio.save()
                except:
                    print('failed to add metadata')
            else:

                print("mp4 metadata")
                print("directory")
                video = EasyMP4(f'{directory}/{video_title} - {resolution}p.mp4')
                print("downloading the thumbnail...")
                download_thumbnail(thumbnail, directory)
                print(video.keys())
                print(video.values())
                print(video.MP4Tags())
                print("adding title")
                video['title'] = video_title
                print("adding artists")
                video['artist'] = artist
                print("adding date")
                video['date'] = date_uploaded[0:4]
                print("adding comment which is link to the youtube video")
                video['comment'] = link
                print(video.keys())
                print(video.values())
                video.save()

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
                        'outtmpl': f'{directory}/{video_title} - {resolution}p.mp4',  # output folder and name
                        'merge_output_format': 'mp4',  # the key name speaks for itself
                        'postprocessors': [{'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'}]
                        # it does require ffmpeg to work.
                    }
                else:
                    quality = quality_choice.get()
                    print(quality)
                    ydl_options = {
                            'format': 'bestaudio/best',
                            'outtmpl': f'{directory}/{video_title} - {quality}kbps',
                            'postprocessors': [{
                                'key': 'FFmpegExtractAudio',
                                'preferredcodec': 'mp3',
                                'preferredquality': f'{quality}'
                            }]
                        }

                # Downloading the video
                with yt_dlp.YoutubeDL(ydl_options) as ydl:
                    ydl.download([f'{link}'])
                metadata_chosen_option = metadata_choice.get()
                if metadata_chosen_option == "yes":
                    with yt_dlp.YoutubeDL() as ydl:
                        info_dict = ydl.extract_info(f'{link}', download=False)
                        artist = info_dict.get('uploader', 'Unknown Artist')
                        print(artist)
                        thumbnail = info_dict.get('thumbnail', 'default.jpg')
                        print(thumbnail)
                        album = info_dict.get('album', 'Unknown album')
                        print(album)
                        genre = info_dict.get('genre', "Unknown genre")
                        print(genre)
                        date_uploaded = info_dict.get('upload_date', None)
                        print(date_uploaded[0:4])
                        length = info_dict.get('duration', 0)
                        print(length)
                #downloading the video metadata
                print("checking the metadata choices...")
                if metadata_chosen_option == "yes":
                    print("adding metadata...")
                    if audio_only:
                        print("audio only metadata...")
                        try:
                            print("specifying the directory of the file")
                            audio = EasyID3(f'{directory}/{video_title} - {quality}kbps.mp3')
                            print("title.")
                            audio['title'] = video_title
                            print("artist")
                            audio['artist'] = artist
                            print("album")
                            audio['album'] = album
                            print("date")
                            audio['date'] = date_uploaded[0:4]
                            print("length")
                            audio['length'] = str(length)
                            print("saving...")
                            print(audio.keys())
                            print(audio.values())
                            audio.save()
                        except:
                            print('failed to add metadata')
                    else:

                        print("mp4 metadata")
                        print("directory")
                        video = EasyMP4(f'{directory}/{video_title} - {resolution}p.mp4')
                        print("downloading the thumbnail...")
                        download_thumbnail(thumbnail, directory)
                        print(video.keys())
                        print(video.values())
                        print(video.MP4Tags())
                        print("adding title")
                        video['title'] = video_title
                        print("adding artists")
                        video['artist'] = artist
                        print("adding date")
                        video['date'] = date_uploaded[0:4]
                        print("adding comment which is link to the youtube video")
                        video['comment'] = link
                        print(video.keys())
                        print(video.values())
                        video.save()
                


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

def show_context_menu(event):
    context_menu.tk_popup(event.x_root, event.y_root)
def paste_text():
    url.event_generate("<<Paste>>")
def cut_text():
    url.event_generate("<<Cut>>")
def copy_text():
    url.event_generate("<<Copy>>")

root = Tk() #creating tkinter object
root.frame() #creating the frame so it could be fullscreened
root.geometry('1053x450')#decided this is an optimal resolution
root.config(bg='#0F0F0F') #setting the background color to the youtube dark mode one
root.title("Youtube Downloader by jtw") #window title
if "yt_icon.ico" in os.listdir(os.getcwd()):
    root.iconphoto(False, PhotoImage(file= f"yt_icon.ico")) #changing the icon of the window to that of
Label(root, text="Youtube Downloader",bg='#0F0F0F',fg='#fafafa' , font='italic 15 bold').pack(pady=10) #first title label

context_menu = Menu(root, tearoff=False)
context_menu.add_command(label="Cut", command=cut_text)
context_menu.add_command(label="Copy", command=copy_text)
context_menu.add_command(label="Paste", command=paste_text)

#Downloadng a single video
Label(root, text = "Download a single video: ",bg='#0F0F0F',fg='#fafafa', font="italic 10").place(relx=0.030, rely=0.155) #label
url = Entry(root, width=60) #creating entry box
url.bind("<Button-3>", show_context_menu)
# url.place(relx=0.35, rely=0.180, anchor=CENTER) #fixed position (would look worse the higher the resolution of the monitor gets)
url.place(relx=0.1783, rely=0.1575) #fixed position (would look worse the higher the resolution of the monitor gets)
# Button(root, text="Download",bg='#267cc7', command=single_video_threading).place(relx=0.559, rely=0.180, anchor=CENTER) #creating the button using random color as background color
Button(root, text="Download",bg='#267cc7', command=single_video_threading).place(relx=0.5285, rely=0.150) #creating the button using random color as background color
download_status = Label(root, text="", bg='#0f0f0f', fg="#fafafa", font='italic 10')
download_status.place(relx=0.1865, rely=0.205) #decided to also add download status for single video downloads

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
# quality_drop.place(relx=0.849, rely=0.347,anchor=CENTER)
quality_drop.place(relx=0.817, rely=0.312)

clicked = StringVar()
clicked.set("1080")
drop = OptionMenu(root, clicked, *resolution_options)
# drop.place(relx=0.630, rely=0.180, anchor=CENTER)
drop.place(relx=0.595, rely=0.145)
drop.config(bg='#0F0F0F', fg='#fafafa', font="italic 10")

#yes or no for subtitles
# Label(root, text = "Do you want to also download subtitle file?", bg='#0F0F0F',fg='#fafafa', font="italic 10", ).place(relx=0.800, rely=0.122, anchor=CENTER)
Label(root, text = "Do you want to also download subtitle file?", bg='#0F0F0F',fg='#fafafa', font="italic 10", ).place(relx=0.689, rely=0.095)
sub_options = ["yes", "no"]
sub_clicked = StringVar()
sub_clicked.set("no")
sub_drop = OptionMenu(root, sub_clicked, *sub_options)
sub_drop.place(relx=0.775, rely=0.145)
sub_drop.config(bg='#0F0F0F', fg='#fafafa', font="italic 10")

# yes or no for audio only download
audio_only_choices = ['yes', 'no']
audio_only_choice = StringVar()
audio_only_choice.set("no")
audio_only_drop = OptionMenu(root, audio_only_choice, *audio_only_choices)

metadata_options = ['yes', 'no']
metadata_choice = StringVar()
metadata_choice.set("yes")
metadata_choice_drop = OptionMenu(root, metadata_choice, *metadata_options)
Label(root, text="Do you want to download the metadata as well?", bg="#0f0f0f", fg="#fafafa", font="italic 10").place(relx=0.6815, rely= 0.450)
metadata_choice_drop.place(relx=0.7850, rely=0.511)
metadata_choice_drop.config(bg='#0F0F0F', fg='#fafafa', font="italic 10")


# Label(root, text= "Do you want to download audio only?", bg="#0f0f0f", fg="#fafafa", font="italic 10").place(relx=0.795, rely=0.287, anchor=CENTER)
Label(root, text= "Do you want to download audio only?", bg="#0f0f0f", fg="#fafafa", font="italic 10").place(relx=0.715, rely=0.255)
# audio_only_drop.place(relx=0.786, rely=0.347, anchor=CENTER)
audio_only_drop.place(relx=0.7555, rely=0.311)
audio_only_drop.config(bg='#0F0F0F', fg='#fafafa', font="italic 10")

#Downloading a playlist
# Label(root, text = "Download a playlist: ",bg='#0F0F0F',fg='#fafafa', font="italic 10").place(relx=0.1, rely=0.350, anchor=CENTER)
Label(root, text = "Download a playlist: ",bg='#0F0F0F',fg='#fafafa', font="italic 10").place(relx=0.030, rely=0.325)
playlist_url = Entry(root, width=60)
playlist_url.bind("<Button-3>", show_context_menu)
playlist_url.place(relx=0.1783, rely= 0.330)
# playlist_url.place(relx=0.349, rely= 0.350, anchor=CENTER)
# Button(root, text="Download", bg='#267cc7', command=playlist_threading).place(relx = 0.557, rely = 0.350, anchor=CENTER)
Button(root, text="Download", bg='#267cc7', command=playlist_threading).place(relx = 0.5285, rely = 0.323)
current_video = Label(root, text='',bg='#0F0F0F', fg='#fafafa', font='italic 10') # not quite sure if I should delete that
current_video.place(relx=0.1865, rely=0.375)

# #creating a progressbar and everything related to it
# progressbar = ttk.Progressbar(root, orient=HORIZONTAL, length=600, mode= 'determinate')
# progressbar.pack(expand=True)
# progressbar.place(x=150, y=235)
progress_percent = Label(root, text='', bg='#0f0f0f', fg='#fafafa', font='italic 10') #progress percent. pretty self explanatory
progress_percent.place(relx=0.1865, rely=0.420)
downloaded = Label(root, text='', bg='#0f0f0f', fg='#fafafa', font='italic 10') #count for downloaded videos
downloaded.place(relx=0.2250, rely=0.420)

#adding the option to change a directory
Label(root, text="Change or add directory",bg='#0F0F0F', fg='#fafafa' ,font='italic 10').place(relx=0.450, rely= 0.665)
new_dir = Entry(root, width=48)
new_dir.bind("<Button-3>", show_context_menu)
new_dir.place(relx=0.375, rely=0.720)
Button(root, text="Change dir",bg='#267cc7', command=directory_change).place(relx=0.480, rely= 0.775)
# Button(root, text="install ffmpeg",bg='#267cc7', command=ffmpeg_install_threading).place(x=600, y= 350)


Button(root, text = "QUIT", font="italic 14 bold", width=8, height=1, bg='RED', fg='#fafafa', command=root.destroy).place(relx= .9, rely=.9, anchor=CENTER)
root.mainloop() #executing tkinter object
