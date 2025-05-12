import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from pytube import YouTube
import threading
import os



class YoutubeDownloader:
    def __init__ (self,root):
        self.root=root
        self.root.title("Youtube Video Downloader")
        self.root.geometry("640x480")
        self.download_path = os.getcwd()

        #For URL
        tk.Label(root,text="Enter Youtube URL: ").pack(pady=4)
        self.urlEntry = tk.Entry(root,width=50)
        self.urlEntry.pack(pady=4)

        #For Quality Selection
        tk.Label(root,text="Select Quality").pack(pady=5)
        self.qualityVar= tk.StringVar(value="720p")
        self.qualityMenu = tk.OptionMenu(root,self.qualityVar,"1080p","720p","480p","360p")
        self.qualityMenu.pack(pady=5)

        #For Folder Selection
        tk.Label(root,text="Download Folder").pack(pady=5)
        self.folderLabel = tk.Label(root,text=self.download_path,wraplength =400)
        self.folderLabel.pack(pady=5)
        tk.Button(root,text="Choose Folder path",command=self.chooseFolder).pack(pady=5)

        #For Download Button
        tk.Button(root,text="Download Video",command=self.startDownload).pack(pady=5)

        #For Status Label
        self.statusLabel = tk.Label(root,text="Enter a URL and the quality you want to Download ",wraplength=400).pack(pady=5)

    def chooseFolder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.download_path = folder
            self.folderLabel.config(text=self.download_path)
            self.statusLabel.config(text=f"Selected Folder = {self.download_path}")

    def startDownload(self):   
        url = self.urlEntry.get().strip()
        if not url:
            self.statusLabel.config(text="Error: Please Enter a valid link")
            return
        
        try:
            self.yt = YouTube(url)
            self.statusLabel.config(text="Starting Download...")
            self.downloadButton=self.root.children['!button2']
            self.downloadButton.config (state = "disabled")
            threading.Thread(self.downloadVideo,daemon=True).start()

        except Exception as e:
            self.statusLabel.config(text=f"Failed To Download Video,Error ({str(e)})")

    def downloadVideo(self):
            try: 
                quality = self.qualityVar.get()
                stream = self.yt.streams.filter(progressive=True,file_extension="mp4",resolution = quality).first()
                if not stream:
                    stream = self.yt.streams.filter(progressive=True,file_extension="mp4",resolution = quality).first()
                    self.root.after(0,lambda:self.statusLabel.config(text= f"Error {quality} stream not available"))
                    if not stream:
                        self.root.after(0,lambda: self.statusLabel.config (text="Error:No valid stream available"))
                        self.root.after(0,lambda: self.downloadButton.config(state ="normal"))
                        return
                    self.root.after(0, lambda: self.statusLabel.config(text=f"Warning: {quality} unavailable, using {stream.resolution}"))
            
                stream.download(output_path=self.download_path)
                self.root.after(0, lambda: self.statusLabel.config(text="Download Complete!"))
                self.root.after(0, lambda: self.downloadButton.config(state="normal"))
            
            except Exception as e:
                self.root.after(0,lambda:self.statusLabel.config(text= f"Error: Download failed ({str(e)})"))
                self.root.after(0, lambda: self.downloadButton.config(state="normal")) 

if __name__ == "__main__":
    root =tk.Tk()
    app = YoutubeDownloader(root)
    root.mainloop()




