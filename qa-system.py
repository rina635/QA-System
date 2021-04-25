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
    
Libraries used: en_core_web_sm, webbrowser, sys, spacy, pprint, bs4,  urllib.request, nltk, sent_tokenize, word_tokenize, RegexpTokenizer, stopwords
Additional features (for extra credit):   
Usage Instructions:     
Algorithm defined in program:
a- Get the question from the user 
b- Check if the question is valid or not. Valid question starts with (who, what, when, or where) and more than three words
c- The log file is created 
d- For each question type:
    1- The keywords of the question are defined after removing the stopwords.
    2- The keywords are used to rewrite the query for searching.
    3- The sentences with keywords and NER tags sapecfied for the question type
        is used to filter the sentence of the returning Wikipedia page 
    4- 3-gram is generated from the filtered sentences.
    5- The n-gram is scored based on criteria givin for each question type. 
    6- The scored n-grams are sorted to be used for n-gram tiling.
    7- The full answer will be returned based on the tiling result. 
e- Unanswered question should be determnined based on the score. If the highest score is 1 means the answer cannot be found. 
f- If the question couldn't be answered, the system will return "I can\'t answer that question. Please try another question."
g- if the user typed "exit", the program will terminaten and the log file will close and show the questions and the answers.     
        

Resources used for this assignment come from the materials provided in the AIT 590 course materials.
- Lecture powerpoints (AIT 590)
- Stanford University Prof. Dan Jurafsky's Video Lectures (https://www.youtube.com/watch?v=zQ6gzQ5YZ8o)
- Joe James Python: NLTK video series (https://www.youtube.com/watch?v=RYgqWufzbA8)
- w3schools Python Reference (https://www.w3schools.com/python/)
- regular expressions 101 (https://regex101.com/)
- https://www.geeksforgeeks.org/python-program-to-convert-a-list-to-string/
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
import operator

#Command line arguments to run file and store user's questions into log file.
#run_file = sys.argv[1]
#log_output = sys.argv[2]

wiki = "https://en.wikipedia.org/w/index.php?search={}"
nlp = en_core_web_sm.load() 

#Retrieve webpage text from Wikipedia site the user's answer leads tos
def scrape_webpage(url):
    url = url.replace(" ", "%20")
    scraped_textdata = urllib.request.urlopen(url)
    textdata = scraped_textdata.read()
    parsed_textdata = bs.BeautifulSoup(textdata,'lxml')
    paragraphs = parsed_textdata.find_all('p')
    formated_text = ""

    for para in paragraphs:
        formated_text += para.text
    
    formated_text = re.sub(r'(\[.*\])', '', formated_text)
    formated_text = formated_text.replace('\n', '')
    return formated_text.encode('ascii', 'ignore')

#Retrieve the entity and its NER 
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

#Retrieve NER for an entity  
def find_ner2(input):
    named_label = ''  
    # Load English tokenizer, tagger, parser, NER and word vectors 
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
def gen_ngrams(query, text, n):
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    tokens = [token for token in text.split(" ") if token != "" and token not in query.split(" ")]
    ngrams = zip(*[tokens[i:] for i in range(n)])
    return [" ".join(ngram) for ngram in ngrams]

#Function to reformulate when question
def when_response(input):
    response = input.replace('?', '')
    if bool(re.match(r"when (was|were)(.*)", input)):
        response = re.sub(r"when (was|were)(.+)", r"\2 \1 ", input) 
    return response

#Function to reformulate where question
def where_response(input):
    response = input.replace('?', '')
    if bool(re.match(r"Where (is|was|were)(.+)", input)):
        response = re.sub(r"Where (is|was|were)(.+)", r"\2 \1 ", response)
    elif bool(re.match(r"Where (was|were)(.+) (discovered|found|created|generated)", input)):
        response = re.sub(r"Where (was|were)(.+) (discovered|found|created|generated)", r"\2 \1 \3 ", response)
    return response

#Function to reformulate what question
def what_response(input):
    response = input.replace('?', '')
    if bool(re.match(r"What (is|was|were|does|did|can|could|should)(.+)", input)):
        response = re.sub(r"What (is|was|were|does|did|can|could|should)(.+)", r"\2 \1 ", response)
    return response

#Function to reformulate who question
def who_response(input):
    response = input.replace('?', '')
    return re.sub(r'Who (is|was|were|can|could|should)(.+)', r'\2 \1 ', response)

# Function to convert list to string  
def listToString(list_element): 
    # initialize an empty string
    text= " " 
    # return string  
    return (text.join(list_element)) 

#https://stackoverflow.com/questions/58151963/how-can-i-take-user-input-and-search-it-in-python

#System can only accept questions that fall into these 4 categories:
#accepted = ['Who', 'What', 'When', 'Where']

#create a logging file
logger = open('log-file.txt','w')
logger.write('Starting New Log.....')

#Function to give the score of the n-gram in Who question
def score_who(ngram):
    score = 0
    who_tag = ["PERSON"]
    title = ["president", "governor", "politician", "ceo", "king", "queen", "prince", "princess", "musician", "actor", "actress", "model", "singer", "author", "writer"]
    for word in ngram.split(" "):
        if word.capitalize():
            score += 1
        if word in title:
            score += 2
    if find_ner2(ngram) in who_tag:
        score += 1
    return score

#Function to give the score of the n-gram in What question
def score_what(ngram):
    score = 0
    what_tag = ["NORP","PRODUCT","EVENT","WORK_OF_ART","LAW","LANGUAGE","PERCENT","MONEY","QUANTITY","ORDINAL","CARDINAL"]
    for word in ngram.split(" "):
        if word.capitalize():
            score += 1
    if find_ner2(ngram) in what_tag:
        score += 1
    return score

#Function to give the score of the n-gram in When question
def score_when(ngram):
    score = 0
    when_tag = ["DATE","TIME"]
    months = ["january","february","march","april","may","june","july","august","september","october","november","december"]
    for word in ngram.split(" "):
        if word.capitalize():
            score += 1
        if word.isdigit():
            score += 2
    if find_ner2(ngram) in when_tag:
        score += 1
    for month in months:
        if month in ngram.lower():
            score += 2
    return score

#Function to give the score of the n-gram in Where question
def score_where(ngram):
    score = 0
    where_tag = ["GPE","ORG","LOC"]
    for word in ngram.split(" "):
        if word.capitalize():
            score += 1
    if find_ner2(ngram) in where_tag:
        score += 2
    return score

def contains_substring(substring, string):
    search = ".*".join(re.escape(word) for word in substring.split(" ")) + ".*"
    return bool(re.search(search.lower(), string.lower()))

def num_substring(substring, string):
    sub = substring.split(" ")
    sent = string.split(" ")
    score = 0
    for word in sent:
        if word in sub:
            score += 1
    return score

# loops until exit
while True:
    #Takes user's input and searches wikipedia
    ask = input('What would you like to learn today?\n')
    #tokenize the question and remove stopwords and use the remaining as keyword to search and filter
    question_tokens = nltk.word_tokenize(ask)
    keywords = [token for token in question_tokens if token not in stopwords.words ('english')]
    
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
        who_tag = ["PERSON", "NORP"]
        query_words = ["was","is","are","were"]
        who_query = []
        for words in query_words:
            who_query.append(text+ " "+words)
        scraped_data = str(scrape_webpage("https://en.wikipedia.org/w/index.php?search={}".format(text)))
        sentences = sent_tokenize(scraped_data)
        filtered_sentences = []
        for sentence in sentences:
            for query in who_query:
                if contains_substring(query, sentence):
                    filtered_sentences.append(sentence)
        ngram_string = " ".join(filtered_sentences)
        ngrams = gen_ngrams(text, ngram_string, 3)
        #url = webbrowser.open("https://en.wikipedia.org/w/index.php?search={}".format(text))
        ngram_score = {}
        for i in ngrams:
            ngram_score[i] = score_who(i)
        ngram_score = dict( sorted(ngram_score.items(), key=operator.itemgetter(1),reverse=True))
        answer = who_response(ask)
        answer += list(ngram_score.keys())[0]
        print(answer)
        
    elif q_type == 'what':
        text, label = find_ner(ask)
        what_tag = ["NORP","PRODUCT","EVENT","WORK_OF_ART","LAW","LANGUAGE","PERCENT","MONEY","QUANTITY","ORDINAL","CARDINAL"]
        query_words = ["was","is","are","were"]
        what_query = []
        for words in query_words:
            what_query.append(text+ " "+words)
        scraped_data = str(scrape_webpage("https://en.wikipedia.org/w/index.php?search={}".format(text)))
        sentences = sent_tokenize(scraped_data)
        filtered_sentences = []
        for sentence in sentences:
            for query in what_query:
                if contains_substring(query, sentence):
                    filtered_sentences.append(sentence)
        ngram_string = "".join(filtered_sentences)
        ngrams = gen_ngrams(text, ngram_string, 3)
        #url = webbrowser.open("https://en.wikipedia.org/w/index.php?search={}".format(text))
        ngram_score = {}
        for i in ngrams:
            ngram_score[i] = score_what(i)
        sorted_ngram_score = dict( sorted(ngram_score.items(), key=operator.itemgetter(1),reverse=True))
        answer = what_response(ask)
        answer += list(ngram_score.keys())[0]
        print(answer)
      
    elif q_type == 'when':
        text, label = find_ner(ask)
        when_tag = ["DATE","TIME"]
        query_words = ["was","is"]
        when_query = []
        for words in query_words:
            when_query.append(text+ " "+words)
        scraped_data = str(scrape_webpage("https://en.wikipedia.org/w/index.php?search={}".format(text)))
        sentences = sent_tokenize(scraped_data)
        filtered_sentences = []
        for sentence in sentences:
            for query in when_query:
                if contains_substring(query, sentence):
                    filtered_sentences.append(sentence)
        ngram_string = "".join(filtered_sentences)
        ngrams = gen_ngrams(text, ngram_string, 3)
        #url = webbrowser.open("https://en.wikipedia.org/w/index.php?search={}".format(text))
        ngram_score = {}
        for i in ngrams:
            ngram_score[i] = score_when(i)
        sorted_ngram_score = dict( sorted(ngram_score.items(), key=operator.itemgetter(1),reverse=True))
        answer = when_response(ask)
        answer += list(ngram_score.keys())[0]
        print(answer)
        
    elif q_type == 'where':
        text, label = find_ner(ask)
        where_tag = ["GPE","ORG","LOC"]
        query_words = ["is in", "is on", "is near", "is next to", "is located"]
        where_query = []
        for words in query_words:
            where_query.append(text+ " "+words)
        scraped_data = str(scrape_webpage("https://en.wikipedia.org/w/index.php?search={}".format(text)))
        sentences = sent_tokenize(scraped_data)
        filtered_sentences = []
        for sentence in sentences:
            for query in where_query:
                if contains_substring(query, sentence):
                    filtered_sentences.append(sentence)
        ngram_string = "".join(filtered_sentences)
        ngrams = gen_ngrams(text, ngram_string, 3)
        #url = webbrowser.open("https://en.wikipedia.org/w/index.php?search={}".format(text))
        ngram_score = {}
        for i in ngrams:
            ngram_score[i] = score_where(i)
        ngram_score = dict( sorted(ngram_score.items(), key=operator.itemgetter(1),reverse=True))
        answer = where_response(ask)
        answer += list(ngram_score.keys())[0]
        print(answer)
        
    else:
        print('I can\'t answer that question. Please try another question.')
    

# close the logging file after everything has been written        
logger.close()
        


# In[4]:





# In[4]:





# In[12]:





# In[ ]:




