import tkinter as tk
from tkinter import filedialog, messagebox
from pytube import YouTube
import os

def download_video():
    url = entry_url.get()
    quality = quality_var.get()
    folder = folder_var.get()
    format_type = format_var.get()

    if not url or not folder:
        messagebox.showwarning("Input Error", "Please enter URL and select a folder.")
        return

    try:
        yt = YouTube(url)
        
        if format_type == "Audio":
            stream = yt.streams.filter(only_audio=True).first()
            out_file = stream.download(output_path=folder)
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            os.rename(out_file, new_file)
        else:
            if quality == "Default":
                stream = yt.streams.get_highest_resolution()
            else:
                stream = yt.streams.filter(res=quality).first()
                if not stream:
                    messagebox.showerror("Error", f"No video stream found for quality: {quality}")
                    return
            stream.download(output_path=folder)
        
        messagebox.showinfo("Success", "Download completed!")
    except Exception as e:
        messagebox.showerror("Error", f"Download failed: {e}")

def select_folder():
    folder = filedialog.askdirectory()
    if folder:
        folder_var.set(folder)

app = tk.Tk()
app.title("YouTube Downloader")

tk.Label(app, text="YouTube URL:").grid(row=0, column=0, padx=10, pady=5)
entry_url = tk.Entry(app, width=50)
entry_url.grid(row=0, column=1, padx=10, pady=5)

tk.Label(app, text="Quality:").grid(row=1, column=0, padx=10, pady=5)
quality_var = tk.StringVar(value="Default")
quality_menu = tk.OptionMenu(app, quality_var, "Default", "1080p", "720p", "480p", "360p", "240p", "144p")
quality_menu.grid(row=1, column=1, padx=10, pady=5)

tk.Label(app, text="Format:").grid(row=2, column=0, padx=10, pady=5)
format_var = tk.StringVar(value="Video")
tk.Radiobutton(app, text="Video", variable=format_var, value="Video").grid(row=2, column=1, sticky='w')
tk.Radiobutton(app, text="Audio", variable=format_var, value="Audio").grid(row=2, column=1, sticky='e')

tk.Label(app, text="Save Folder:").grid(row=3, column=0, padx=10, pady=5)
folder_var = tk.StringVar()
tk.Entry(app, textvariable=folder_var, width=50).grid(row=3, column=1, padx=10, pady=5)
tk.Button(app, text="Select Folder", command=select_folder).grid(row=3, column=2, padx=10, pady=5)

tk.Button(app, text="Download", command=download_video).grid(row=4, column=0, columnspan=3, pady=10)

app.mainloop()
