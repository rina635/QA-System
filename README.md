# QA-System
AIT 590 - Assignment 4: Question & Answer System
Team 3 - Rafeef Baamer, Ashish Hingle, Rina Lidder, & Andy Nguyen
Date: 4/21/2021
Description: This is a QA system by  Rafeef Baamer, Ashish Hingle, Rina Lidder, & Andy Nguyen. 
It will try to answer questions that start with Who, What, When or Where. Enter "exit" to leave the program.
            
Types of questions: Who - When - What- Where
 
Example: 
    Question: Who is George Washington?
    Answer: George Washington is the first president of the United States
How to run: python qa-system.py
Libraries used: en_core_web_sm, webbrowser, sys, spacy, pprint, bs4,  urllib.request, nltk, sent_tokenize, word_tokenize, RegexpTokenizer, stopwords
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
    7- The full answer will be returned based on the tiling result with a word cloud image for the common words in the Wikipedia page. 
e- Unanswered question should be determnined based on the score. If the highest score is 1 means the answer cannot be found. 
f- If the question couldn't be answered, the system will return "I can\'t answer that question. Please try another question."
g- if the user typed "exit", the program will terminaten and the log file will close and show the questions and the answers.     
Function for Extra Credit: 
We created a function that show word cloud image for the words in the Wikipedia page that is related to the question. 
Resources used for this assignment come from the materials provided in the AIT 590 course materials.
- Lecture powerpoints (AIT 590)
- Stanford University Prof. Dan Jurafsky's Video Lectures (https://www.youtube.com/watch?v=zQ6gzQ5YZ8o)
- Joe James Python: NLTK video series (https://www.youtube.com/watch?v=RYgqWufzbA8)
- w3schools Python Reference (https://www.w3schools.com/python/)
- regular expressions 101 (https://regex101.com/)
- https://www.geeksforgeeks.org/python-program-to-convert-a-list-to-string/
- https://stackoverflow.com/questions/16645799/how-to-create-a-word-cloud-from-a-corpus-in-python
