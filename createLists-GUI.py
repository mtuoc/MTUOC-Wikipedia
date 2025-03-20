#    createLists-GUI
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

from tkinter import *
from tkinter.ttk import *

import tkinter 
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import askdirectory
from tkinter import messagebox

import sqlite3
import codecs
import sys
 
# Define a dictionary with category namespaces for different languages
category_namespaces = {
    "en": "Category",
    "ceb": "Kategoriya",
    "de": "Kategorie",
    "fr": "Catégorie",
    "sv": "Kategori",
    "nl": "Categorie",
    "ru": "Категория",
    "it": "Categoria",
    "es": "Categoría",
    "pl": "Kategoria",
    "ja": "カテゴリ",
    "vi": "Thể loại",
    "war": "Kaarangay",
    "zh": "分类",
    "uk": "Категорія",
    "ar": "تصنيف",
    "pt": "Categoria",
    "fa": "رده",
    "ca": "Categoria",
    "sr": "Категорија",
    "id": "Kategori",
    "ko": "분류",
    "no": "Kategori",
    "fi": "Luokka",
    "hu": "Kategória",
    "cs": "Kategorie",
    "ro": "Categorie",
    "tr": "Kategori",
    "eu": "Kategoria",
    "eo": "Kategorio",
    "da": "Kategori",
    "bg": "Категория",
    "sk": "Kategória",
    "kk": "Санат",
    "he": "קטגוריה",
    "lt": "Kategorija",
    "hr": "Kategorija",
    "az": "Kateqoriya",
    "sl": "Kategorija",
    "et": "Kategooria",
    "el": "Κατηγορία",
    "gl": "Categoría",
    "simple": "Category",
    "th": "หมวดหมู่",
    "sh": "Kategorija",
    "be": "Катэгорыя",
    "ms": "Kategori",
    "ka": "კატეგორია",
    "hi": "श्रेणी",
    "mk": "Категорија",
    "bs": "Kategorija",
    "af": "Kategorie",
    "uz": "Turkum",
    "bn": "বিষয়শ্রেণী",
    "lv": "Kategorija",
    "hy": "Կատեգորիա",
    "tt": "Төркем",
    "ur": "زمرہ",
    "azb": "بؤلمه",
    "ta": "பகுப்பு",
    "be-tarask": "Катэгорыя",
    "zh-min-nan": "分類",
    "te": "వర్గం",
    "tl": "Kategorya",
    "jv": "Kategori",
    "oc": "Categoria",
    "tg": "Гурӯҳ",
    "su": "Kategori",
    "kn": "ವರ್ಗ",
    "mg": "Sokajy",
    "mi": "Rōpū",
    "arz": "تصنيف",
    "scn": "Categoria",
    "sa": "वर्गः",
    "ne": "श्रेणी",
    "ckb": "پۆل",
    "gd": "Roinn-seòrsa",
    "ht": "Kategori",
    "mr": "वर्ग",
    "sq": "Kategori",
    "is": "Flokkur",
    "so": "Qeyb",
    "cy": "Categori",
    "br": "Rummad",
    "co": "Categoria",
    "szl": "Kategoria",
    "tk": "Kategoriýa",
    "pnb": "زمرہ",
    "sw": "Jamii",
    "fj": "Wase",
    "lrc": "پۆل",
    "dv": "ޤިސްމު",
    "nah": "Neneuhcāyōtl",
    "bat-smg": "Kateguorėjė",
    "bug": "Kategori",
    "cu": "Катигорїꙗ",
    "kw": "Class",
    "gv": "Ronney",
    "lez": "Категория",
    "ab": "Категориа",
    "bm": "Catégorie",
    "tyv": "Категория",
    "ve": "Konḓwa",
    "sn": "Chikamu",
    "pi": "विभागो",
    "iu": "ᑎᑎᕋᐅᓯᔭᖅ",
    "ny": "Gulu",
    "min": "Kategori",
    "zu": "Isigaba",
    "qu": "Katiguriya",
    "fy": "Kategory",
    "sah": "Категория",
    "kl": "Sumut ataqatigiissut",
    "kab": "Awrir",
    "haw": "Māhele",
    "ln": "Catégorie",
    "ug": "تۈر",
    "an": "Categoría",
    "mwl": "Categoria",
    "bi": "Kategori",
    "st": "Sehlopha",
    "li": "Categorie",
    "mt": "Kategorija",
    "tpi": "Kategri",
    "hsb": "Kategorija",
    "to": "Vahe",
    "ki": "Kĩrĩ",
    "yo": "Ẹ̀ka",
    "tw": "Nkyekyɛmu",
    "mg": "Sokajy",
    "tyv": "Категория",
    "ve": "Konḓwa",
    "tum": "Tchingwe",
    "lo": "ປະເພດ",
    "lad": "Kateggoría",
    "csb": "Kategòrëjô",
    "as": "শ্ৰেণী",
    "rw": "Icyiciro",
    "xh": "Udidi",
    "ts": "Xikategoria",
    "tn": "Setlhopha",
    "tk": "Kategoriýa",
    "tw": "Nkyekyɛmu",
    "wa": "Categoreye",
    "wo": "Wàll",
    "wuu": "分类",
    "xh": "Udidi",
    "yi": "קאַטעגאָריע",
    "yo": "Ẹ̀ka",
    "diq": "Kategoriye",
    "zap": "Ninyakayu",
    "sn": "Chikamu",
    "za": "分類",
    "zu": "Isigaba",
    "ast": "Categoría"
}

def select_database():
    inputfile = askopenfilename(initialdir = ".",filetypes =(("SQLite files", ["*.sqlite"]),("All Files","*.*")),
                           title = "Choose a database to use.")
    E1.delete(0,END)
    E1.insert(0,inputfile)
    E1.xview_moveto(1)
    
def select_category_list():
    categorylistfile = asksaveasfilename(initialdir = ".",filetypes =(("text files", ["*.txt"]),("All Files","*.*")),
                           title = "Choose a file to save the category list.")
    E5.delete(0,END)
    E5.insert(0,categorylistfile)
    E5.xview_moveto(1)
    
def select_title_list():
    titlelistfile = asksaveasfilename(initialdir = ".",filetypes =(("text files", ["*.txt"]),("All Files","*.*")),
                           title = "Choose a file to save the title list.")
    E6.delete(0,END)
    E6.insert(0,titlelistfile)
    E6.xview_moveto(1)
    
def select_output():
    outputdir = askdirectory(initialdir = ".",mustexist=False, title = "Choose the output directory.")
    E5.delete(0,END)
    E5.insert(0,outputdir)
    E5.xview_moveto(1)




def create_lists():
    categories=[]
    categoriesTEMP=[]
    categoriesAUX=[]
    todownload=[]
    database=E1.get()
    categoria=E2.get()
    depth=E3.get()
    category_list_file=E5.get()
    title_list_file=E6.get()
    if depth==None: depth=1
    try:
        depth=int(depth)
    except:
        depth=1
    lang=E4.get()
    try:
        allCategories=False
        if categoria=="*" or categoria=="All" or categoria=="all":
            allCategories=True
        else:
            categories = [cat.strip() for cat in categoria.split(",")]
            categories_temp = categories[:]
            categories_aux = []
        
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        categoryprefix=category_namespaces[lang]+":"
        titles = []    
        if not allCategories:
            while depth > 0:
                while categories_temp:
                    category = categories_temp.pop(0)
                    cur.execute('SELECT categoryREL FROM categoryrelations WHERE category=?', (category,))
                    data = cur.fetchall()
                    for d in data:
                        categories.append(d[0])
                        categories_aux.append(d[0])
                categories_temp.extend(categories_aux)
                categories_aux = []
                depth -= 1

            idents = {}
            with codecs.open(category_list_file, "w", encoding="utf-8") as cf:
                for category in categories:
                    cf.write(category + "\n")
                    cur.execute('SELECT ident FROM categories WHERE category=?', (category,))
                    data = cur.fetchall()
                    for d in data:
                        idents[d[0]] = 1

            
            if not allCategories:
                with codecs.open(title_list_file, "w", encoding="utf-8") as tf:
                    if lang != "en":
                        for ident in idents:
                            cur.execute('SELECT title FROM langlinks WHERE ident=? AND lang=?', (ident, lang))
                            data = cur.fetchone()
                            if not data==None:
                                if not data[0].startswith(categoryprefix):
                                    titles.append(data[0])
                                    tf.write(data[0]+"\n")
                    else:
                        for ident in idents:
                            cur.execute('SELECT title FROM titles WHERE ident=?', (str(ident),))
                            data = cur.fetchone()
                            if not data==None:
                                if not data[0].startswith(categoryprefix):
                                    titles.append(data[0])
                                    tf.write(data[0]+"\n")
        else:
            with codecs.open(title_list_file, "w", encoding="utf-8") as tf:
                if lang != "en":
                    cur.execute('SELECT title FROM langlinks WHERE lang=?', (lang,))
                    data = cur.fetchall()
                    
                    if not data==None:
                        for d in data:
                            if not d[0].startswith(categoryprefix):
                                titles.append(d[0])
                                tf.write(d[0]+"\n")
                else:
                    cur.execute('SELECT title FROM titles')
                    data = cur.fetchall()
                    if not data==None:
                        for d in data:
                            if not d[0].startswith(categoryprefix):
                                titles.append(d[0])
                                tf.write(d[0]+"\n")
        E7.delete(0,END)
        if not allCategories:
            E7.insert(0,len(categories))
        E8.delete(0,END)
        E8.insert(0,len(titles))
        try:
            cf.close()
        except:
            pass
        try:
            tf.close()
        except:
            pass

    except Exception as e:
        messagebox.showerror("Error", sys.exc_info())
        

categories=[]
categoriesTEMP=[]
categoriesAUX=[]
todownload=[]


top = Tk()
top.title("createLists-GUI")

B1=tkinter.Button(top, text = str("Select Database"), borderwidth = 1, command=select_database,width=20).grid(row=0,column=0)
E1 = tkinter.Entry(top, bd = 5, width=50, justify="right")
E1.grid(row=0,column=1)

L2 = Label(top,text="Categories:").grid(sticky="E",row=1,column=0)
E2 = tkinter.Entry(top, bd = 5, width=50, justify="left")
E2.grid(row=1,column=1)

L3 = Label(top,text="Depth:").grid(sticky="E",row=2,column=0)
E3 = tkinter.Entry(top, bd = 5, width=3, justify="left")
E3.grid(sticky="W",row=2,column=1)

L4 = Label(top,text="Lang:").grid(sticky="E",row=3,column=0)
E4 = tkinter.Entry(top, bd = 5, width=3, justify="left")
E4.grid(sticky="W",row=3,column=1)

B5=tkinter.Button(top, text = str("Select category list file"), borderwidth = 1, command=select_category_list,width=20).grid(row=4,column=0)
E5 = tkinter.Entry(top, bd = 5, width=50, justify="left")
E5.grid(row=4,column=1)

E5.delete(0,END)
E5.insert(0,"category-list.txt")

B6=tkinter.Button(top, text = str("Select title list file"), borderwidth = 1, command=select_title_list,width=20).grid(row=5,column=0)
E6 = tkinter.Entry(top, bd = 5, width=50, justify="left")
E6.grid(row=5,column=1)

E6.delete(0,END)
E6.insert(0,"title-list.txt")

L7 = Label(top,text="TOTAL CATEGORIES:").grid(sticky="E",row=6,column=0)
E7 = tkinter.Entry(top, bd = 5, width=20, justify="right")
E7.grid(sticky="W",row=6,column=1)

L8 = Label(top,text="TOTAL TITLES:").grid(sticky="E",row=7,column=0)
E8 = tkinter.Entry(top, bd = 5, width=20, justify="right")
E8.grid(sticky="W",row=7,column=1)



B9=tkinter.Button(top, text = str("Create lists!"), borderwidth = 1, command=create_lists,width=20).grid(row=8,column=0)


E1.delete(0,END)
E1.xview_moveto(1)

E2.delete(0,END)
E2.xview_moveto(1)


    
top.mainloop()
