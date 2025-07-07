import json
import sqlite3
from colorama import *

conn = sqlite3.connect("urls.db")
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM urls")
nb_urls = cursor.fetchone()[0]
conn.close()

print("Nombre d'urls total :", nb_urls)

conn = sqlite3.connect("words.db")
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM words")
nb_words = cursor.fetchone()[0]
conn.close()

print("Nombre de mots :", nb_words)

with open("urls_stack.txt", 'r', encoding="utf-8") as file:
    data = file.read()

print("Nombre d'urls en attentes : ", len(data))

import stanza
from langdetect import detect
from functools import lru_cache

# Langues supportées par Stanza (tu peux en ajouter ou retirer selon ton projet)
SUPPORTED_LANGS = {
    "en", "fr", "es", "de", "it", "pt", "ru", "zh", "ar", "nl", "sv", "fi", "no", "tr"
}

@lru_cache(maxsize=32)  # pour ne pas recharger les modèles à chaque appel
def load_pipeline(lang):
    stanza.download(lang, verbose=False)
    return stanza.Pipeline(lang=lang, processors="tokenize,mwt,pos,lemma", use_gpu=False)

def lemmatize_multilang(text):
    try:
        lang = detect(text)
    except:
        return {"lang": None, "error": "Langue non détectée", "lemmas": []}

    if lang not in SUPPORTED_LANGS:
        return {"lang": lang, "error": f"Langue non supportée : {lang}", "lemmas": []}

    try:
        nlp = load_pipeline(lang)
        doc = nlp(text)
        lemmas = [word.lemma for sent in doc.sentences for word in sent.words]
        return {"lang": lang, "lemmas": lemmas}
    except Exception as e:
        return {"lang": lang, "error": str(e), "lemmas": []}

texts = [
    "Les enfants jouent dans le jardin.",
    "The children are playing in the garden.",
    "Los niños juegan en el jardín.",
    "Die Kinder spielen im Garten."
]

for txt in texts:
    result = lemmatize_multilang(txt)
    print(f"[{result['lang']}] → {result['lemmas']}")
