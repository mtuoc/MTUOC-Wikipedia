#!/usr/bin/python3
#    translateTitleList-GUI
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

import sqlite3
import os
import codecs
import tkinter as tk
from tkinter import filedialog, messagebox

def ensure_indices(cursor, indices):
    for index_name, index_sql in indices.items():
        cursor.execute("""
            SELECT COUNT(1) 
            FROM sqlite_master 
            WHERE type='index' AND name=?;
        """, (index_name,))
        exists = cursor.fetchone()[0]
        if not exists:
            print(f"Creating index: {index_name}")
            cursor.execute(index_sql)

def go():
    try:
        required_indices = {
            "titles_title_idx": "CREATE INDEX IF NOT EXISTS titles_title_idx ON titles(title);",
            "langlinks_ident_idx": "CREATE INDEX IF NOT EXISTS langlinks_ident_idx ON langlinks(ident);",
            "langlinks_title_idx": "CREATE INDEX IF NOT EXISTS langlinks_title_idx ON langlinks(title);"
        }

        print("Verifying indexes.")
        ensure_indices(cur, required_indices)
        conn.commit()

        entrada = codecs.open(input_file_path.get(), "r", encoding="utf-8")
        output = codecs.open(output_file_path.get(), "w", encoding="utf-8")
        control = []

        for line in entrada:
            line = line.strip()
            cur.execute('SELECT ident FROM langlinks WHERE title=? AND lang=?', (line, source_lang.get()))
            data = cur.fetchall()

            for d in data:
                ident = d[0]
                if target_lang.get() == "en":
                    cur2.execute('SELECT title FROM titles WHERE ident=?', (ident,))
                else:
                    cur2.execute('SELECT title FROM langlinks WHERE ident=? AND lang=?', (ident, target_lang.get()))

                data2 = cur2.fetchall()
                for d2 in data2:
                    if d2[0] not in control:
                        print(d2[0])
                        output.write(f"{d2[0]}\n")
                        control.append(d2[0])

        messagebox.showinfo("Success", "Translation completed successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        entrada.close()
        output.close()

# GUI Setup
root = tk.Tk()
root.title("Wikipedia Title Translator")

# Variables
database_file_path = tk.StringVar()
input_file_path = tk.StringVar()
output_file_path = tk.StringVar()
source_lang = tk.StringVar()
target_lang = tk.StringVar()

# Functions for file selection
def select_database():
    file_path = filedialog.askopenfilename(filetypes=[("SQLite Database", "*.db, *.sqlite"), ("All Files", "*.*")])
    if file_path:
        database_file_path.set(file_path)

def select_input_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        input_file_path.set(file_path)

def select_output_file():
    file_path = filedialog.asksaveasfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        output_file_path.set(file_path)

def start_translation():
    if not database_file_path.get() or not input_file_path.get() or not output_file_path.get() or not source_lang.get() or not target_lang.get():
        messagebox.showerror("Error", "All fields are required.")
        return

    try:
        global conn, cur, cur2
        conn = sqlite3.connect(database_file_path.get())
        cur = conn.cursor()
        cur2 = conn.cursor()

        go()

    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        if conn:
            conn.close()

# Layout
frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill="both", expand=True)

tk.Label(frame, text="Database File:").grid(row=0, column=0, sticky="e")
tk.Entry(frame, textvariable=database_file_path, width=40).grid(row=0, column=1)
tk.Button(frame, text="Browse", command=select_database).grid(row=0, column=2)

tk.Label(frame, text="Input File:").grid(row=1, column=0, sticky="e")
tk.Entry(frame, textvariable=input_file_path, width=40).grid(row=1, column=1)
tk.Button(frame, text="Browse", command=select_input_file).grid(row=1, column=2)

tk.Label(frame, text="Output File:").grid(row=2, column=0, sticky="e")
tk.Entry(frame, textvariable=output_file_path, width=40).grid(row=2, column=1)
tk.Button(frame, text="Browse", command=select_output_file).grid(row=2, column=2)

tk.Label(frame, text="Source Language:").grid(row=3, column=0, sticky="e")
tk.Entry(frame, textvariable=source_lang, width=10).grid(row=3, column=1, sticky="w")

tk.Label(frame, text="Target Language:").grid(row=4, column=0, sticky="e")
tk.Entry(frame, textvariable=target_lang, width=10).grid(row=4, column=1, sticky="w")

tk.Button(frame, text="Start Translation", command=start_translation).grid(row=5, column=0, columnspan=3, pady=10)

root.mainloop()
