import sqlite3
import bz2
import argparse
import mwparserfromhell
import mwxml
import xml.etree.ElementTree as ET

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

def parse_wikipedia_dump(dump_path, database_path):
    """Procesa el dump de Wikipedia y almacena los artículos en la base de datos."""
    create_database(database_path)

    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    batch_size = 1000
    articles = []
    cont=0
    title = None
    text = None
    with bz2.open(dump_path, 'rb') as f:
        # Parse the dump file
        dump = mwxml.Dump.from_file(f)
        
        # Iterate over each page in the dump
        for page in dump:
            title=page.title
            cont+=1
            
            for revision in page:
                text = extract_text_from_wikitext(revision.text)
            
            if title and text:
                articles.append((title, text))
                
            if len(articles) >= batch_size:
                cursor.executemany("INSERT OR IGNORE INTO articles (title, content) VALUES (?, ?)", articles)
                conn.commit()
                articles.clear()  

            title = None
            text = None
                
    conn.close()

def main():
    parser = argparse.ArgumentParser(description="Processes a Wikipedia dump to create a SQLite database with titles and texts.")
    parser.add_argument("--dump", required=True, help="Wikipedia dump file in .bz2")
    parser.add_argument("--database", required=True, help="SQLite database")

    args = parser.parse_args()

    parse_wikipedia_dump(args.dump, args.database)

if __name__ == "__main__":
    main()
