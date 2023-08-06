# -*- coding: utf-8 -*-
"""
Created on Fri May  5 01:14:04 2023

@author: Narjes
"""

import streamlit as st
import deep_translator
from langdetect import detect
import re 
import codecs
import numpy as np
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import feature_extraction 
from sklearn import linear_model
from sklearn import pipeline 
from sklearn.model_selection import train_test_split 
from sklearn import metrics
import string
import pickle 

# Détection automatique de langue
def lang_detect(text):
    global lrLangDetectModel
    lrLangDetectFile = open('model.pckl', 'rb')
    lrLangDetectModel = pickle.load(lrLangDetectFile)
    lrLangDetectFile.close()
    
    text = "".join(text.split())
    text = text.lower()
    text = re.sub(r"\d+", "", text)
    translate_table = dict((ord(char), None) for char in string.punctuation)
    text = text.translate(translate_table)
    pred = lrLangDetectModel.predict([text])
    prob = lrLangDetectModel.predict_proba([text])
    return pred[0]

# Interface utilisateur
st.title("Traducteur Anglais-Arabe")

# Détection de la langue
def detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown"

# Interface utilisateur
st.subheader("Entrez le texte à traduire:")
text = st.text_area("")

# Détection de la langue et traduction
if st.button("Traduire"):
    source_lang = detect_language(text)
    target_lang = "ar" if source_lang == "en" else "en"
    translated_text = deep_translator.GoogleTranslator(source=source_lang, target=target_lang).translate(text)
    st.write("Langue source:", source_lang)
    st.write("Langue cible:", target_lang)
    st.write("Texte traduit:", translated_text)

# Assistant vocal
if st.button("Assistant vocal"):
    st.write("Fonctionnalité d'assistant vocal à venir bientôt!")
    
# Détection automatique de langue
if st.button("Détecter la langue"):
    detected_lang = lang_detect(text)
    st.write("Langue détectée:", detected_lang)
