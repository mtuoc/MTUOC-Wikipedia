import sqlite3
import bz2
import mwparserfromhell
import mwxml
import tkinter as tk
from tkinter import filedialog, messagebox
import threading

def create_database(database_path):
    """Crea la base de datos SQLite con una tabla indexada."""
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            text TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_title
        ON articles (title)
    """)

    conn.commit()
    conn.close()

# Function to extract plain text from wikitext
def extract_text_from_wikitext(wikitext):
    wikicode = mwparserfromhell.parse(wikitext)
    return wikicode.strip_code()

def parse_wikipedia_dump(dump_path, database_path, update_progress):
    """Procesa el dump de Wikipedia y almacena los artículos en la base de datos."""
    
    if os.path.exists(database_path):
        os.remove(database_path)
    
    create_database(database_path)

    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    batch_size = 1000
    articles = []
    cont = 0

    with bz2.open(dump_path, 'rb') as f:
        # Parse the dump file
        dump = mwxml.Dump.from_file(f)

        # Iterate over each page in the dump
        for page in dump:
            title = page.title
            cont += 1

            for revision in page:
                text = extract_text_from_wikitext(revision.text)

            if title and text:
                articles.append((title, text))

            if len(articles) >= batch_size:
                cursor.executemany("INSERT OR IGNORE INTO articles (title, text) VALUES (?, ?)", articles)
                conn.commit()
                articles.clear()

            update_progress(f"Processsing: {cont} pages processed.")

    # Insert remaining articles
    if articles:
        cursor.executemany("INSERT OR IGNORE INTO articles (title, text) VALUES (?, ?)", articles)
        conn.commit()

    conn.close()

def start_processing(dump_path, database_path, progress_label):
    def update_progress(message):
        progress_label.config(text=message)

    def process():
        try:
            parse_wikipedia_dump(dump_path, database_path, update_progress)
            update_progress("Process completed.")
            messagebox.showinfo("Success", "The dump has been processed and stored in the database.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    threading.Thread(target=process).start()

def select_file(entry):
    file_path = filedialog.askopenfilename(filetypes=[("Wikipedia dump", "*.bz2")])
    if file_path:
        entry.delete(0, tk.END)
        entry.insert(0, file_path)

def save_file(entry):
    file_path = filedialog.asksaveasfilename(defaultextension=".db", filetypes=[("SQLite database", "*.sqlite"),("SQLite database", "*.db"),("All files", "*.*")])
    if file_path:
        entry.delete(0, tk.END)
        entry.insert(0, file_path)

def main():
    root = tk.Tk()
    root.title("createWikipediaDatabase-GUI")

    tk.Label(root, text="Wikipedia dump (.bz2):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
    dump_entry = tk.Entry(root, width=50)
    dump_entry.grid(row=0, column=1, padx=5, pady=5)
    tk.Button(root, text="Select", command=lambda: select_file(dump_entry)).grid(row=0, column=2, padx=5, pady=5)

    tk.Label(root, text="SQLite database:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
    db_entry = tk.Entry(root, width=50)
    db_entry.grid(row=1, column=1, padx=5, pady=5)
    tk.Button(root, text="Select", command=lambda: save_file(db_entry)).grid(row=1, column=2, padx=5, pady=5)

    progress_label = tk.Label(root, text="Progress: Waiting start...", fg="blue")
    progress_label.grid(row=2, column=0, columnspan=3, padx=5, pady=10)

    tk.Button(root, text="Start", command=lambda: start_processing(dump_entry.get(), db_entry.get(), progress_label)).grid(row=3, column=0, columnspan=3, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
