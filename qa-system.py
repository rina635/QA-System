#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 20:35:57 2021

@author: Rina
"""
import webbrowser
import sys
import spacy
from pprint import pprint
import bs4 as bs  # BeautifulSoup
import urllib.request

#Command line arguments to run file and store user's questions into log file.
run_file = sys.argv[1]
log_output = sys.argv[2]

#Retrieve webpage text from Wikipedia site the user's answer leads tos
def scrape_webpage(url):
    scraped_textdata = urllib.request.urlopen(url)
    textdata = scraped_textdata.read()
    parsed_textdata = bs.BeautifulSoup(textdata,'lxml')
    paragraphs = parsed_textdata.find_all('p')
    formated_text = ""

    for para in paragraphs:
        formated_text += para.text
    
    return formated_text

#https://stackoverflow.com/questions/58151963/how-can-i-take-user-input-and-search-it-in-python
#Takes user's input and searches wikipedia
ask = input('What would you like to learn today?\n')
print(ask)
#Use tagger on user input then use that as the variable to search wikipedia for

url = webbrowser.open("https://en.wikipedia.org/w/index.php?search={}".format(ask))

#Scrapes the text from wikipedia site
web_text = scrape_webpage(url)
#Generates webpage's named entities.
pprint([(X.text, X.label_) for X in url.ents])

#Will extrace Part-of-speech of sentences from webpage
#https://spacy.io/usage/spacy-101
for sentences in web_text:
    print(sentences.txt, sentences.pos_)