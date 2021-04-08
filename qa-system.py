#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 20:35:57 2021

@author: Rina
"""
import webbrowser
import sys

#Command line arguments to run file and store user's questions into log file.
run_file = sys.argv[1]
log_output = sys.argv[2]


#https://stackoverflow.com/questions/58151963/how-can-i-take-user-input-and-search-it-in-python
#Takes user's input and searches wikipedia
ask = input('What would you like to learn today?\n')
print(ask)
webbrowser.open("https://en.wikipedia.org/w/index.php?search={}".format(ask))

