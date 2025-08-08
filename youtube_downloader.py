import os
import tkinter as tk
from tkinter import filedialog, messagebox
from yt_dlp import YoutubeDL
from threading import Thread

class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")
        self.root.geometry("600x460")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e1e")  # Dark background

        self.default_font = ("Segoe UI", 10)
        self.button_color = "#2d89ef"
        self.bg_color = "#1e1e1e"
        self.fg_color = "#ffffff"
        self.entry_bg = "#2d2d2d"
        self.entry_fg = "#ffffff"
        self.highlight_color = "#3a9efb"

        # --- URL Input ---
        self.url_label = tk.Label(root, text="YouTube URL:", bg=self.bg_color, fg=self.fg_color, font=self.default_font)
        self.url_label.pack(pady=(15, 5))

        self.url_entry = tk.Entry(root, width=60, bg=self.entry_bg, fg=self.entry_fg,
                                  insertbackground="white", relief=tk.FLAT, font=self.default_font)
        self.url_entry.pack(pady=5, ipady=5)

        # --- Fetch Button ---
        self.fetch_button = tk.Button(root, text="🎯 Fetch Formats", command=self.fetch_formats,
                                      bg=self.button_color, fg="white", font=self.default_font,
                                      relief=tk.FLAT, activebackground=self.highlight_color)
        self.fetch_button.pack(pady=8, ipadx=5, ipady=3)

        # --- Format Listbox ---
        self.format_listbox = tk.Listbox(root, width=80, height=10, bg=self.entry_bg, fg=self.fg_color,
                                         selectbackground=self.highlight_color, font=("Consolas", 9),
                                         relief=tk.FLAT, borderwidth=0)
        self.format_listbox.pack(pady=10)

        # --- Save Location Button ---
        self.save_button = tk.Button(root, text="📁 Select Save Location", command=self.select_location,
                                     bg=self.button_color, fg="white", font=self.default_font,
                                     relief=tk.FLAT, activebackground=self.highlight_color)
        self.save_button.pack(pady=5, ipadx=5, ipady=3)

        # --- Path Label ---
        self.save_path_label = tk.Label(root, text="Save Location: Not selected",
                                        bg=self.bg_color, fg="#aaaaaa", font=("Segoe UI", 9, "italic"))
        self.save_path_label.pack(pady=2)

        # --- Download Button (Hidden initially) ---
        self.download_button = tk.Button(root, text="⬇️ Download Selected Format", command=self.download_thread,
                                         bg="#28a745", fg="white", font=self.default_font,
                                         relief=tk.FLAT, activebackground="#34d058")
        self.download_button.pack(pady=15, ipadx=5, ipady=5)
        self.download_button.pack_forget()

        # Variables
        self.save_path = ""
        self.formats = []
        self.video_info = None

    def fetch_formats(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showerror("Error", "Please enter a valid URL.")
            return

        self.format_listbox.delete(0, tk.END)

        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'forcejson': True,
            'noplaylist': True,
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                self.video_info = ydl.extract_info(url, download=False)
                self.formats = self.video_info.get("formats", [])

                for f in self.formats:
                    if f.get('filesize'):
                        size = round(f['filesize'] / (1024 * 1024), 2)
                        label = f"{f['format_id']} - {f['ext']} - {f.get('resolution', 'audio')} - {size} MB"
                    else:
                        label = f"{f['format_id']} - {f['ext']} - {f.get('resolution', 'audio')}"

                    self.format_listbox.insert(tk.END, label)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch formats:\n{str(e)}")

    def select_location(self):
        folder = filedialog.askdirectory()
        if folder:
            self.save_path = folder
            self.save_path_label.config(text=f"Save Location: {self.save_path}", fg="#44ff88")
            self.download_button.pack(pady=15, ipadx=5, ipady=5)

    def download_thread(self):
        Thread(target=self.download_video).start()

    def download_video(self):
        selection = self.format_listbox.curselection()
        if not selection:
            messagebox.showwarning("Select Format", "Please select a format to download.")
            return

        if not self.save_path:
            messagebox.showwarning("Save Location", "Please select a save location first.")
            return

        format_id = self.formats[selection[0]]['format_id']
        url = self.url_entry.get()

        ydl_opts = {
            'format': format_id,
            'outtmpl': os.path.join(self.save_path, '%(title)s.%(ext)s'),
            'noplaylist': True,
            'quiet': False,
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            messagebox.showinfo("Success", f"✅ Download completed!\n📂 Saved to:\n{self.save_path}")
        except Exception as e:
            messagebox.showerror("Download Failed", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloader(root)
    root.mainloop()
