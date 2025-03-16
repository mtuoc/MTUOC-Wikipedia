#    createLists
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

import argparse
import sqlite3
import codecs
import sys

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

def create_lists(database, categories, depth, lang, category_list_file, title_list_file):
    try:
        categories = [cat.strip() for cat in categories.split(",")]
        categories_temp = categories[:]
        categories_aux = []
        
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        categoryprefix=category_namespaces[lang]+":"
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

        titles = []
        idents = list(idents.keys())
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

        print(f"Total categories: {len(categories)}")
        print(f"Total titles: {len(titles)}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create category and title lists from a database.")
    parser.add_argument("-d", "--database", required=True, help="Path to the SQLite database file.")
    parser.add_argument("-c", "--categories", required=True, help="Comma-separated list of categories to start with.")
    parser.add_argument("--depth", type=int, required=True, help="Depth of category relations.")
    parser.add_argument("--lang", required=True, help="Language code.")
    parser.add_argument("-cl", "--category_list", default="category-list.txt", help="Output file for the category list.")
    parser.add_argument("-tl", "--title_list", default="title-list.txt", help="Output file for the title list.")

    args = parser.parse_args()

    create_lists(
        database=args.database,
        categories=args.categories,
        depth=args.depth,
        lang=args.lang,
        category_list_file=args.category_list,
        title_list_file=args.title_list
    )
