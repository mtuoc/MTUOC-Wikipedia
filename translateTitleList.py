#!/usr/bin/python3
#    translateTitleList
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
import sys
import argparse


    

def ensure_indices(cursor, indices):
    for index_name, index_sql in indices.items():
        # Verificar si el índice ya existe
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
    required_indices = {
    "titles_title_idx": "CREATE INDEX IF NOT EXISTS titles_title_idx ON titles(title);",
    "langlinks_ident_idx": "CREATE INDEX IF NOT EXISTS langlinks_ident_idx ON langlinks(ident);",
    "langlinks_title_idx": "CREATE INDEX IF NOT EXISTS langlinks_title_idx ON langlinks(title);"
    }
    
    print("Verifying indexes.")
    ensure_indices(cur, required_indices)

    # Confirmar los cambios
    conn.commit()

    global sl
    global tl
    global inputfile
    global lang
    
    entrada=codecs.open(inputfile,"r",encoding="utf-8")
    control=[]
    for linia in entrada:
        linia=linia.strip()
        #select ident from langlinks where title="Filosofía" and lang="an";
        cur.execute('SELECT ident from langlinks WHERE title=? and lang=?', (linia,sl))
        data=cur.fetchall()
        for d in data:
            ident=d[0]
            if tl=="en":
                #select title from titles where ident="13692155";
                cur2.execute('SELECT title from titles WHERE ident=?', (ident,))
                data2=cur2.fetchall()
                for d in data2:
                    if not d[0] in control:
                        print(d[0])     
                        sortida.write("d[0]\n")
                        control.append(d[0])
            else:
                #select * from langlinks where ident="13692155" and lang="ru";
                cur2.execute('SELECT title from langlinks WHERE ident=? and lang=?', (ident,tl))
                data2=cur2.fetchall()
                for d in data2:
                    if not d[0] in control:
                        print(d[0])     
                        sortida.write("d[0]\n")
                        control.append(d[0])
        

if __name__ == "__main__":        
    parser = argparse.ArgumentParser(description='Translates a list of wikipedia titles')
    
    parser.add_argument("-d",'--database', action="store", dest="filename", help='The CCW sqlite database to use.',required=True)

    parser.add_argument("-i",'--input', action="store", dest="inputfile", help='The text file containing the list of titles to translate',required=True)

    parser.add_argument('--sl', action="store", dest="sl", help='The source language code.',required=True)
    
    parser.add_argument('--tl', action="store", dest="tl", help='The target language code.',required=True)
        
    parser.add_argument("-o",'--output', action="store", dest="outputfile", help='The path of the output file.',required=True)
        
    args = parser.parse_args()  
    
    filename=args.filename

    conn=sqlite3.connect(filename)
    cur = conn.cursor() 
    cur2 = conn.cursor() 
    inputfile=args.inputfile
    outputfile=args.outputfile
    
    sl=args.sl
    tl=args.tl
    
    sortida=codecs.open(outputfile,"w",encoding="utf-8")
    
 
    go()