import sqlite3
import codecs
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def go(database, outdir, titlesfile):
    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()

        with codecs.open(titlesfile, "r", encoding="utf-8") as entrada:
            for linia in entrada:
                title = linia.strip()
                aux = title.replace(" ", "_").replace("/", "_").replace("\\", "_") + ".txt"
                outfilename = os.path.join(outdir, aux)

                with codecs.open(outfilename, "w", encoding="utf-8") as sortida:
                    cur.execute('SELECT text FROM articles WHERE title=?', (title,))
                    data = cur.fetchall()
                    for d in data:
                        text = d[0]
                        sortida.write(title + "\n")
                        sortida.write(text + "\n")

        messagebox.showinfo("Success", "Processing completed successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

def select_database():
    filepath = filedialog.askopenfilename(title="Select SQLite Database", filetypes=[("SQLite files", "*.db *.sqlite")])
    db_entry.delete(0, tk.END)
    db_entry.insert(0, filepath)

def select_titlesfile():
    filepath = filedialog.askopenfilename(title="Select Titles File", filetypes=[("Text files", "*.txt")])
    titles_entry.delete(0, tk.END)
    titles_entry.insert(0, filepath)

def select_outdir():
    directory = filedialog.askdirectory(title="Select Output Directory")
    outdir_entry.delete(0, tk.END)
    outdir_entry.insert(0, directory)

def start_processing():
    database = db_entry.get()
    titlesfile = titles_entry.get()
    outdir = outdir_entry.get()

    if not os.path.exists(database):
        messagebox.showerror("Error", "Database file does not exist!")
        return
    if not os.path.exists(titlesfile):
        messagebox.showerror("Error", "Titles file does not exist!")
        return
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    go(database, outdir, titlesfile)

# Create main window
root = tk.Tk()
root.title("Wikipedia Dump to Text Converter")

# Database file selection
tk.Label(root, text="SQLite Database:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
db_entry = tk.Entry(root, width=50)
db_entry.grid(row=0, column=1, padx=10, pady=5)
db_button = tk.Button(root, text="Browse", command=select_database)
db_button.grid(row=0, column=2, padx=10, pady=5)

# Titles file selection
tk.Label(root, text="Titles File:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
titles_entry = tk.Entry(root, width=50)
titles_entry.grid(row=1, column=1, padx=10, pady=5)
titles_button = tk.Button(root, text="Browse", command=select_titlesfile)
titles_button.grid(row=1, column=2, padx=10, pady=5)

# Output directory selection
tk.Label(root, text="Output Directory:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
outdir_entry = tk.Entry(root, width=50)
outdir_entry.grid(row=2, column=1, padx=10, pady=5)
outdir_button = tk.Button(root, text="Browse", command=select_outdir)
outdir_button.grid(row=2, column=2, padx=10, pady=5)

# Start processing button
process_button = tk.Button(root, text="Start Processing", command=start_processing)
process_button.grid(row=3, column=0, columnspan=3, pady=20)

# Run the application
root.mainloop()
