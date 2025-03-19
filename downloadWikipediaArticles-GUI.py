#!/usr/bin/python3
#    downloadWikipediaArticles
#    Copyright (C) 2025  Antoni Oliver
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import codecs
import sys
import wikipedia
import tkinter as tk
from tkinter import filedialog, messagebox

def go(titleList, lang, outdir):
    todownload = []
    try:
        with codecs.open(titleList, "r", encoding="utf-8") as alf:
            for linia in alf:
                linia = linia.strip()
                todownload.append(linia)

        if not os.path.exists(outdir):
            os.makedirs(outdir)

        wikipedia.set_lang(lang)
        for td in todownload:
            outfile = os.path.join(outdir, td.replace(" ", "_").replace("/", "-") + ".txt")
            print(td)
            try:
                with codecs.open(outfile, "w", encoding="utf-8") as sortida:
                    page = wikipedia.page(td)
                    sortida.write(page.content + "\n")
            except Exception as e:
                print(f"ERROR DOWNLOADING {td}: {e}")

        messagebox.showinfo("Success", "Articles downloaded successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI Setup
root = tk.Tk()
root.title("Wikipedia Articles Downloader")

# Variables
title_file_path = tk.StringVar()
output_dir_path = tk.StringVar()
language = tk.StringVar()

# Functions for file selection
def select_title_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        title_file_path.set(file_path)

def select_output_dir():
    dir_path = filedialog.askdirectory()
    if dir_path:
        output_dir_path.set(dir_path)

def start_download():
    if not title_file_path.get() or not output_dir_path.get() or not language.get():
        messagebox.showerror("Error", "All fields are required.")
        return

    go(title_file_path.get(), language.get(), output_dir_path.get())

# Layout
frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill="both", expand=True)

tk.Label(frame, text="Title List File:").grid(row=0, column=0, sticky="e")
tk.Entry(frame, textvariable=title_file_path, width=40).grid(row=0, column=1)
tk.Button(frame, text="Browse", command=select_title_file).grid(row=0, column=2)

tk.Label(frame, text="Output Directory:").grid(row=1, column=0, sticky="e")
tk.Entry(frame, textvariable=output_dir_path, width=40).grid(row=1, column=1)
tk.Button(frame, text="Browse", command=select_output_dir).grid(row=1, column=2)

tk.Label(frame, text="Language Code:").grid(row=2, column=0, sticky="e")
tk.Entry(frame, textvariable=language, width=10).grid(row=2, column=1, sticky="w")

tk.Button(frame, text="Start Download", command=start_download).grid(row=3, column=0, columnspan=3, pady=10)

root.mainloop()
