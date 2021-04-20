#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AIT 590 - Assignment 4
Team 3 - Rafeef Baamer, Ashish Hingle, Rina Lidder, & Andy Nguyen
Date: 4/21/2021
Description:
Types of questions:
    
Libraries used: 
Additional features (for extra credit):    
Usage Instructions:     
Algorithm defined in program:
    
Resources used for this assignment come from the materials provided in the AIT 590 course materials.
- Lecture powerpoints (AIT 590)
- Stanford University Prof. Dan Jurafsky's Video Lectures (https://www.youtube.com/watch?v=zQ6gzQ5YZ8o)
- Joe James Python: NLTK video series (https://www.youtube.com/watch?v=RYgqWufzbA8)
- w3schools Python Reference (https://www.w3schools.com/python/)
- regular expressions 101 (https://regex101.com/)
"""
import en_core_web_sm
import webbrowser
import sys
import spacy
import re
from pprint import pprint
import bs4 as bs  # BeautifulSoup
import urllib.request
from spacy import displacy
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords

#Command line arguments to run file and store user's questions into log file.
#run_file = sys.argv[1]
#log_output = sys.argv[2]

wiki = "https://en.wikipedia.org/w/index.php?search={}"

#Retrieve webpage text from Wikipedia site the user's answer leads tos
def scrape_webpage(url):
    url = url.replace(" ", "%20")
    scraped_textdata = urllib.request.urlopen(url)
    textdata = scraped_textdata.read()
    parsed_textdata = bs.BeautifulSoup(textdata,'lxml')
    #paragraphs = parsed_textdata.find_all('p')
    paragraphs = parsed_textdata.find_all('p')
    formated_text = ""

    for para in paragraphs:
        formated_text += para.text
    
    formated_text = re.sub(r'(\[.*\])', '', formated_text)
    formated_text = formated_text.replace('\n', '')
    return formated_text.encode('ascii', 'ignore')

#Retrieve NER 
def find_ner(input):
    
    named_text = ''
    named_label = ''
    
    # Load English tokenizer, tagger, parser, NER and word vectors
    nlp = en_core_web_sm.load()
  
    # transform the text to spacy doc format
    mytext = nlp(input)
    
    for ent in mytext.ents:
        named_text = ent.text
        named_label = ent.label_
        
        #print(ent.text, ent.start_char, ent.end_char, ent.label_)

    return named_text, named_label

#Retrieve NER 
def find_ner2(input):
    named_label = ''
    
    # Load English tokenizer, tagger, parser, NER and word vectors
    nlp = en_core_web_sm.load()
  
    # transform the text to spacy doc format
    mytext = nlp(input)
    
    for ent in mytext.ents:
        named_label = ent.label_
        
    return named_label

# checks the type of question
question_words = ["who", "when", "where", "what"]

#Check the question type and length. If the question in less than three words or starts with other than (who, when, where, what) words
#the question will be considered invalid 
def check_q_type(question):
    question = question.lower()
    question_token = word_tokenize(question)
    question_word = question_token[0]
    if question_word not in question_words and len(question_token) < 3:
        print("This is invalid question")
    else:
        if question_word == "who":
            return 'who'
        elif question_word == "when":
            return 'when'
        elif question_word == "where":
            return 'where'
        elif question_word == "what":
            return 'what'

#Function to generate n-gram 
def gen_ngrams(text, n):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    tokens = [token for token in text.split(" ") if token != ""]
    ngrams = zip(*[tokens[i:] for i in range(n)])
    return [" ".join(ngram) for ngram in ngrams]

#Function to reformulate when question
def when_query(input):
    if input == r"when (was|were)(.*)":
        input = r"\2 \1" 
    return input

#Function to reformulate where question
def where_query(input):
    if input == r"where (was|were)(.*)":
        input = r"\2 \1" 
    elif input == r"where (was|were)(.*) (discovered|found|created|generated)":
        input = (r"\2 \1 \3", 4)
    return input

#Function to reformulate what question
def where_query(input):
    if input == r"what (is|was|were|does|did|can|could|should)(.*)":
        input = r"\2 \1" 
    return input

#Function to reformulate who question
def where_query(input):
    if input == r"who (is|was|were|can|could|should)(.*)":
        input = r"\2 \1" 
    return input

#https://stackoverflow.com/questions/58151963/how-can-i-take-user-input-and-search-it-in-python

#System can only accept questions that fall into these 4 categories:
#accepted = ['Who', 'What', 'When', 'Where']

#create a logging file
logger = open('log-file.txt','w')
logger.write('Starting New Log.....')


# loops until exit
while True:
    #Takes user's input and searches wikipedia
    ask = input('What would you like to learn today?\n')
    #tokenize the question and removve stopwords and use the remaining as keyword to search and filter
    question_tokens = nltk.word_tokenize(ask)
    keywords = [token for token in  question_tokens if token not in stopwords.words ('english')]
    
    # add to log file
    logger.write('\n' + ask)
    
    if (ask == 'exit'):
        print('we will now exit')
        break
    
    #check the type of question   
    q_type = check_q_type(ask.lower())
    #print(q_type)
    
    # logic for if a input is a who question
    if q_type == 'who':
        
        # find any text and labels NER
        text, label = find_ner(ask)
        scraped_data = str(scrape_webpage("https://en.wikipedia.org/w/index.php?search={}".format(text)))
        sentences = sent_tokenize(scraped_data)
        filtered_sentences = []
        for sentence in sentences:
            if text in sentence:
                for keyword in keywords:
                    if keyword in sentence:
                        filtered_sentences.append(sentence)
        print(filtered_sentences)
        ngram_string = "".join(filtered_sentences)
        ngrams = gen_ngrams(ngram_string, 3)
        print(ngrams)
        print(text, label)
        url = webbrowser.open("https://en.wikipedia.org/w/index.php?search={}".format(text))
            
        
    elif q_type == 'what':
        text, label = find_ner(ask)
        what_tag = ["NORP","PRODUCT","EVENT","WORK_OF_ART","LAW","LANGUAGE","PERCENT","MONEY","QUANTITY","ORDINAL","CARDINAL"]
        scraped_data = str(scrape_webpage("https://en.wikipedia.org/w/index.php?search={}".format(text)))
        sentences = sent_tokenize(scraped_data)
        #keywords = ["was", "is"]
        filtered_sentences = []
        for sentence in sentences:
            if text in sentence:
                for keyword in keywords:
                    if keyword in sentence:
                        filtered_sentences.append(sentence)
        print(filtered_sentences)
        ngram_string = "".join(filtered_sentences)
        ngrams = gen_ngrams(ngram_string, 3)
        print(ngrams)
        print(text, label)
        url = webbrowser.open("https://en.wikipedia.org/w/index.php?search={}".format(text))
        
    elif q_type == 'when':
        text, label = find_ner(ask)
        when_tag = ["DATE","TIME"]
        scraped_data = str(scrape_webpage("https://en.wikipedia.org/w/index.php?search={}".format(text)))
        sentences = sent_tokenize(scraped_data)
        #keywords = ["was", "is", "from"]
        #keywords = when_query(ask)
        filtered_sentences = []
        for sentence in sentences:
            if text in sentence:
                for keyword in keywords:
                    if keyword in sentence and find_ner2(sentence) in when_tag):
                        filtered_sentences.append(sentence)
        print(filtered_sentences)
        ngram_string = "".join(filtered_sentences)
        ngrams = gen_ngrams(ngram_string, 3)
        print (keywords)
        print(ngrams)
        print(text, label)
        url = webbrowser.open("https://en.wikipedia.org/w/index.php?search={}".format(text))
        
    elif q_type == 'where':
        text, label = find_ner(ask)
        where_tag = ["GPE","ORG","LOC"]
        scraped_data = str(scrape_webpage("https://en.wikipedia.org/w/index.php?search={}".format(text)))
        sentences = sent_tokenize(scraped_data)
        #keywords = ["was", "is", "near"]
        filtered_sentences = []
        for sentence in sentences:
            if text in sentence:
                for keyword in keywords:
                    if keyword in sentence and (find_ner2(sentence) == "GPE" or find_ner2(sentence) == "ORG" or find_ner2(sentence) == "LOC"):
                        filtered_sentences.append(sentence)
        print(filtered_sentences)
        ngram_string = "".join(filtered_sentences)
        ngrams = gen_ngrams(ngram_string, 3)
        print(ngrams)
        print(text, label)
        url = webbrowser.open("https://en.wikipedia.org/w/index.php?search={}".format(text))
        
    else:
        print('I can\'t answer that question. Please try another question.')
    

# close the logging file after everything has been written        
logger.close()
        
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


# In[ ]:





# In[ ]:




