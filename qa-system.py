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
#run_file = sys.argv[1]
#log_output = sys.argv[2]

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

#System can only accept questions that fall into these 4 categories:
#accepted = ['Who', 'What', 'When', 'Where']

#Takes user's input and searches wikipedia
ask = input('What would you like to learn today?\n')
print(ask)
url = webbrowser.open("https://en.wikipedia.org/w/index.php?search={}".format(ask))
'''
#Check if its an acceptable question
if ask[0] in accepted:
    #Then take question and use POS Tagger/NER to extract the main points its abouut
    #Process it and then use that as the input for the wikipedia search

#Use tagger on user input then use that as the variable to search wikipedia for
elif ask[0] == 'exit':
    print('Thank you! Goodbye.')
else:
    print("I am sorry, I don't know the answer")    
    




#Scrapes the text from wikipedia site
web_text = scrape_webpage(url)
#Generates webpage's named entities.
pprint([(X.text, X.label_) for X in url.ents])

#Will extrace Part-of-speech of sentences from webpage
#https://spacy.io/usage/spacy-101
for sentences in web_text:
    print(sentences.txt, sentences.pos_)
'''    