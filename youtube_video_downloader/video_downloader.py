
import tkinter as tk
import os
import youtube_dl
import tkinter.font as tkfont
from tkinter import *
from tkinter.ttk import *

root = tk.Tk()
root.title('Video Downloader')
root.geometry('400x400')
root.resizable(width=FALSE,height=FALSE)

canvas1 = tk.Canvas(root,height = 400, width=400, bg="#000d00")
canvas1.pack()
bold_font = tkfont.Font(family="Helvetica",size=12,weight="bold")
label1 = tk.Label(root,text= "Enter the URL",width=20,bg="#900d42")
label1.config(font=bold_font)
canvas1.create_window(200,100,window=label1)
download_entry = tk.Entry(root)
canvas1.create_window(200,140,window=download_entry)

def get_video_url():
   search_item = download_entry.get()
   ydl_opts = {
      'format': 'best',
      'noplaylist': True,
      'extract-audio': True,
   }
   os.chdir('downloads/')
   with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([search_item])
   bold_font2 = tkfont.Font(family="Helvetica",size=10,weight="bold")
   label2 =tk.Label(root,text="Video Downloaded",width=20,bg="#263d42")
   label2.config(font=bold_font2)
   canvas1.create_window(200,300,window=label2)

download = tk.Button(text= "Download", padx=5,pady=5,fg = "white",bg = "DeepSkyBlue4",command = get_video_url)
canvas1.create_window(200,230,window=download)
root.mainloop()