import sqlite3
import sys
import argparse
import codecs
import os


def go():
    entrada=codecs.open(titlesfile,"r",encoding="utf-8")
    for linia in entrada:
        title=linia.strip()
        aux=title+".txt"
        outfilename=os.path.join(outdir,aux)
        sortida=codecs.open(outfilename,"w",encoding="utf-8")
        cur.execute('SELECT text from articles WHERE title=?', (title,))
        data=cur.fetchall()
        for d in data:
            text=d[0]
            print(title)
            sortida.write(title+"\n")
            print(text)
            sortida.write(text+"\n")
            print("-----")
        sortida.close()

    
parser = argparse.ArgumentParser(description='Script to convert Wikipedia dumps to text files from a list of titles')
parser.add_argument('-d','--database', action="store", dest="database", help='The wikipedia database create from de dump file.',required=True)
parser.add_argument('-o','--outdir', action="store", dest="outdir", help='The output directory.',required=True)
parser.add_argument('-t','--titlesfile', action="store", dest="titlesfile", help='A file where the converted article titles will be stored. By default titles-list.txt.',required=False)

args = parser.parse_args()
database = args.database
conn=sqlite3.connect(database)
cur = conn.cursor() 
outdir=args.outdir
if not os.path.exists(outdir):
    os.makedirs(outdir)

titlesfile=args.titlesfile



go()