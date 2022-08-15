import sys
# from pytube import YouTube
import pytube
from pytube import Playlist
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import requests




def percent(tem, total):
    perc = (float(tem) / float(total)) * float(100)
    return perc


def on_progress(vid, chunk, bytes_remaining):
    total_size = vid.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    totalsz = (total_size/1024)/1024
    totalsz = round(totalsz,1)
    remain = (bytes_remaining / 1024) / 1024
    remain = round(remain, 1)
    dwnd = (bytes_downloaded / 1024) / 1024
    dwnd = round(dwnd, 1)
    percentage_of_completion = round(percentage_of_completion,2)

    #print(f'Total Size: {totalsz} MB')
    print(f'Download Progress: {percentage_of_completion}%, Total Size:{totalsz} MB, Downloaded: {dwnd} MB, Remaining:{remain} MB')


def on_complete(stream, filename):
    print()
    print('--- Downloaded ---')
    print('= Video title:', stream.title)
    print('= File size:',round(stream.filesize/1024/1024, 2),'MB')

def find_qualitiest_streams(playlist):
    chosen_streams = []
    i = 0
    for video in playlist.videos:
        chosen_streams.append(None)
        streams = video.streams.filter(only_audio=True)
        for stream in streams:
            if "mp4" in stream.mime_type:
                stream_bitrate = int(stream.abr[0:-4])
                if chosen_streams[i] is None or stream_bitrate > int(chosen_streams[i].abr[0:-4]):
                    chosen_streams[i] = stream
        i += 1

    return chosen_streams

def get_streams_total_size(streams):
    total = 0
    for stream in streams:
        total += stream.filesize
    return total



"""def download_playlist(save_path, link):
    SAVE_PATH = "~/Music/"
    link = "https://www.youtube.com/watch?v=dGAxojETm9A"
    p_link = 'https://www.youtube.com/watch?v=irZ2dA9nQIM&list=OLAK5uy_mjaIMROwYq9eGXGoc7LEoB7FABy6SJYxg'

    try:
        p = Playlist(p_link)
    except:
        print("Connection Error")  # to handle exception
        sys.exit(0)

    for video in p.videos:
        try:
            selected_stream = video.streams.filter(only_audio=True).first()
            video.register_on_progress_callback(on_progress)
            video.register_on_complete_callback(on_complete)
            selected_stream.download()
        except:
            print("Connection Error")
"""


if __name__ == '__main__':
    master_window = tk.Tk()
    master_window.title("YT Playlist Download")
    master_window.columnconfigure([0, 1, 2], weight=1)
    master_window.rowconfigure([0, 1, 2, 3, 4, 5, 6, 7], weight=1)

    df_location = 'NOT SELECTED!'
    playlist_object = pytube.Playlist

    lbl_form_dirselect1 = tk.Label(text="Download folder: ", anchor=tk.E)
    lbl_form_dirselect1.grid(row=0, column=0, padx=10, pady=10)

    lbl_form_dirselect2 = tk.Label(text=df_location, anchor=tk.E)
    lbl_form_dirselect2.grid(row=0, column=1, padx=10, pady=10)

    prepare_progress_bar = ttk.Progressbar(master_window, orient="horizontal", mode="indeterminate", length=300)
    prepare_progress_bar.grid(row=7, column=0, padx=10, pady=10, columnspan=3)
    prepare_progress_bar.grid_forget()

    def loader_wrapper():
        print("ahoj")
        master_window.after(0, prepare_progress_bar.grid(row=7, column=0, padx=10, pady=10, columnspan=3))
        prepare_progress_bar.start()
        analyze_playlist()

    def ask_directory(event=None):
        df_location = filedialog.askdirectory()
        lbl_form_dirselect2.config(text="Download folder: " + df_location)

    btn_form_dirselect = tk.Button(text="Select", command=ask_directory, anchor=tk.W)
    btn_form_dirselect.grid(row=0, column=2, padx=10, pady=10)

    lbl_form_playlist = tk.Label(text="Playlist URL: ", anchor=tk.E)
    lbl_form_playlist.grid(row=1, column=0, padx=10, pady=10)

    ent_form_playlist = tk.Entry()
    ent_form_playlist.grid(row=1, column=1, padx=10, pady=10)

    sorted_streams = []
    total_size = None
    to_download_mb = None

    def analyze_playlist(event=None):
        lbl_playlist_error.grid_forget()
        lbl_playlist_title.grid_forget()
        btn_playlist_download.grid_forget()
        try:
            p = Playlist(ent_form_playlist.get())

            global sorted_streams, total_size, to_download_mb
            sorted_streams = find_qualitiest_streams(p)
            total_size = get_streams_total_size(sorted_streams)
            to_download_mb = round(total_size / 1024 / 1024, 2)

            print(p.videos[0].thumbnail_url)
            new_video_image_obj = Image.open(requests.get(p.videos[0].thumbnail_url, stream=True).raw)
            new_video_image_obj.thumbnail((350, 350))
            new_playlist_image = ImageTk.PhotoImage(new_video_image_obj)
            lbl_playlist_image.config(image=new_playlist_image)
            lbl_playlist_image.image = new_playlist_image

            lbl_playlist_title.config(text=p.title)
            lbl_playlist_title.grid(row=5, column=0, padx=10, pady=10, columnspan=3)

            prepare_progress_bar.grid_forget()
            btn_playlist_download.grid(row=6, column=1, padx=10, pady=10)
            global playlist_object
            playlist_object = p

        except:
            lbl_playlist_error.config(text="PLAYLIST ERROR!")
            lbl_playlist_error.grid(row=3, column=0, padx=10, pady=10, columnspan=3)

        #lbl_playlist_error.grid(row=3, column=0, padx=10, pady=10, columnspan=3)

    btn_playlist_load = tk.Button(text="Load playlist", command=loader_wrapper, anchor=tk.W)
    btn_playlist_load.grid(row=2, column=1, padx=10, pady=10)

    lbl_playlist_error = tk.Label(text="ERROR", fg='red')
    lbl_playlist_error.grid(row=3, column=0, padx=10, pady=10, columnspan=3)
    lbl_playlist_error.grid_forget()

    video_image_obj = Image.open("placeholder.jpg")
    video_image_obj.thumbnail((350, 350))
    playlist_image = ImageTk.PhotoImage(video_image_obj)
    lbl_playlist_image = tk.Label(image=playlist_image, anchor=tk.NE)
    lbl_playlist_image.image = playlist_image

    lbl_playlist_image.grid(row=4, column=0, padx=10, pady=10, columnspan=3)

    lbl_playlist_title = tk.Label(text="placeholder")
    lbl_playlist_title.grid(row=5, column=0, padx=10, pady=10, columnspan=3)
    lbl_playlist_title.grid_forget()

    def download_playlist(playlist, sorted_streams, to_download):
        prepare_progress_bar.grid(row=7, column=0, padx=10, pady=10, columnspan=3)
        to_download_count = len(sorted_streams)
        downloaded = 0
        downloaded_mb = 0

        download_window = tk.Toplevel(master_window)
        download_window.columnconfigure([0, 1, 2], weight=1)
        download_window.rowconfigure([0, 1, 2, 3, 4, 5, 6], weight=1)

        lbl_download_count_label = tk.Label(download_window, text="Videos downloaded:")
        lbl_download_count_label.grid(row=0, column=0, padx=10, pady=10)
        lbl_download_count = tk.Label(download_window,
                                      text=str(downloaded) + '/' + str(to_download_count))
        lbl_download_count.grid(row=0, column=1, padx=10, pady=10)

        lbl_download_total_filesize_label = tk.Label(download_window, text="Downloaded:")
        lbl_download_total_filesize_label.grid(row=1, column=0, padx=10, pady=10)
        lbl_download_total_filesize_count = tk.Label(download_window,
                                      text=str(downloaded_mb) + 'MB/' + str(to_download_mb) + 'MB')
        lbl_download_total_filesize_count.grid(row=1, column=1, padx=10, pady=10)

        lbl_download_downloading_song = tk.Label(download_window, text=playlist.videos[0].title)
        lbl_download_downloading_song.grid(row=3, column=0, padx=10, pady=10, columnspan=2)

        progress_bar = ttk.Progressbar(download_window, orient="horizontal", mode="determinate", length=300)
        progress_bar.grid(row=4, column=0, padx=10, pady=10, columnspan=2)
        progress_bar['value'] = 10

        btn_download_start_download = tk.Button(download_window, text="Start")
        btn_download_start_download.grid(row=5, column=1, padx=10, pady=10, columnspan=2)




    btn_playlist_download = tk.Button(text="Download", command= lambda : download_playlist(playlist_object, sorted_streams, total_size))
    btn_playlist_download.grid(row=6, column=1, padx=10, pady=10)
    btn_playlist_download.grid_forget()





    master_window.mainloop()





