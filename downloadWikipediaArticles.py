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
import argparse


def go():
    global outdir
    global titleList
    global lang
    todownload=[]
    alf=codecs.open(titleList,"r",encoding="utf-8")
    
    for linia in alf:
        linia=linia.strip()
        todownload.append(linia)
    
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    
    wikipedia.set_lang(lang)
    for td in todownload:
        outfile=outdir+"/"+td.replace(" ","_").replace("/","-")+".txt"
        print(td)
        try:
            sortida=codecs.open(outfile,"w",encoding="utf-8")
            page = wikipedia.page(td)
            sortida.write(page.content+"\n")
        except:
            print("ERROR DOWNLOADING ",td,sys.exc_info()[0])
    alf.close()


if __name__ == "__main__":        
    parser = argparse.ArgumentParser(description='Script for the creation of parallel corpora from Wikipedia')
    
    parser.add_argument('--tl', action="store", dest="titleList", help='The file containing the list of titles to download.',required=True)
    
    parser.add_argument('--lang', action="store", dest="lang", help='The language (two letter ISO code used in Wikipedia).',required=True)
        
    parser.add_argument("-o",'--output', action="store", dest="outdir", help='The path to the output dir where the article files will be stored (if it does\'nt exist, it is created).',required=True)
    
    args = parser.parse_args()  

    titleList=args.titleList
    lang=args.lang
    outdir=args.outdir
    
    go()