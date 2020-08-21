# NLP-Final-Project
This is the final project for Whitman CS 357 Natural Language Processing (2019 Fall). 
Created by Tracy Cui and Tina Tao


Summary:
This project is aiming to add a language model of POS tagging into the SpellChecker program. Our program is able to first detect the incorrect words in the text and then replace the incorrect words with the correct words with the highest probability according to the pos tagging. The text could be both a sentence or a list of sentences. 


Reference/Sources:
We used Python built-in Spell Checker (pyspellchecker) to recognize the incorrect words and to generate a list of possible words for each incorrect word
Use “pip install pyspellchecker” to download the package

Corpora used:
We used Brown corpus from NLTK as our training set for probability calculation. This corpus contains lists of list of words with tags
We used the Holbrook-tagged.dat corpus as our training set. This corpus contained sentences with incorrect words and their corrections (https://www.dcs.bbk.ac.uk/~roger/corpora.html) 
