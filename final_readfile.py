import numpy as np
import re
from spellchecker import SpellChecker
import nltk
import pickle

#Global Variables 
fp = open('final_model.dat', 'rb')
model = pickle.load(fp)
#print(model)
A = model[0]
B = model[1]
T = model[2]

#return lists of list of sentences with wrong words and a dictionary of correct words 
def getlines(file):
    text = []
    f = open(file, 'r')
    for line in f:
        sentence = line.split()
        text.append(sentence)

    errordic = {}
    errornum = 0
    for sentence in text:
        # move ERR
        for x in range(2): #check again as some error will occur when a <ERR> next to another <ERR>
            for word in sentence:
                if word[0] == '<':
                    sentence.remove(word)
                
        # save all correct spellchecker result
        for word in sentence:
            if word[0:5] == 'targ=':
                errornum += 1
                if text.index(sentence) not in errordic:
                    errordic[text.index(sentence)] = [word[5:(len(word)-1)]]
                else:
                    errordic[text.index(sentence)].append(word[5:(len(word)-1)])
                #errors.append([text.index(sentence), word[5:(len(word)-1)]])
                sentence.remove(word)

        # deal with punctuation
        for word in sentence:
            if word[-1] in ".,!>?'" and word.count('.') < 2:
                if len(word) == 1:
                    sentence.remove(word)
                else:
                    sentence[sentence.index(word)] = word[:(len(word)-1)]
        #print(sentence)

    #print(errordic)

    return text, errordic, errornum




#calculate the possibility of one possible sentence
def prob(W):
    vit = {}

    #bp = [0 for i in range(len(W))]
    #N = len(T)
    #v_tw = 0
    max_prob = float("-inf")
    for i in range(len(W)):
        if i == 0:
            for t in T:
                vit[t] = {}
                try:
                    vit[t][W[0]] = A['<s>'][t] + B[t][W[0]]
                    #bp[0] = t

                except KeyError:
                    vit[t][W[0]] = float("-inf")

            #print(vit)

        else:
        #bp[W[i]] = {}
            for t in T:
                vit[t][W[i]] = float("-inf")
                #print(vit)
                for tprev in T:
                    try:
                        v_tw = vit[tprev][W[i-1]] + A[tprev][t] + B[t][W[i]]

                    except KeyError:
                        v_tw = float("-inf")
                        
                    if v_tw > vit[t][W[i]]:
                        vit[t][W[i]] = v_tw
                        if vit[t][W[i]] > max_prob:
                            max_prob = vit[t][W[i]]
                
    return max_prob


def findError(sentence):
    #print(sentence)
    newline = []
    spell = SpellChecker()
    for word in sentence:
        if word.islower() == True:
            newline.append(word)
    #print(newline)
    errors = spell.unknown(newline)
    #print(errors)
    index = []
    for word in errors:
        index.append(sentence.index(word))
    return index

def get_possibles(sentence):
    spell = SpellChecker()
    newline = []
    for word in sentence:
        if word.islower() == True:
            newline.append(word)
    errors = spell.unknown(newline)
    
    if len(errors) == 0:
        return [sentence]
    else:
        first = errors.pop()
        checkword = spell.candidates(first)
        check = [sentence]*len(checkword)
        index = sentence.index(first)
        newlist = []
        for element in check:
            element[index] = checkword.pop()
            newlist.append(element[:])

        ret_list = []
        for sent in newlist:
            ret_list.extend(get_possibles(sent))
        #print(ret_list)
        
    return ret_list
        

#import a list of words and return a list of corrected words with highest possibilities and a list of corrected text
def correction(sentence):
    indexes = findError(sentence)
    #incorrect_word_count = len(indexes)
    possible_sents = get_possibles(sentence)
    #print(possible_sents) 
    #print(indexes)
    max_prob = float("-inf")
    max_prob_sent = []
    corrected_words = []
    for sent in possible_sents:
        probability = prob(sent)
        #print(probability)
        if probability > max_prob:
            max_prob = probability
            #print(max_prob)
            max_prob_sent = sent[:] 
    #print(max_prob_sent)
    for i in indexes:
        corrected_words.append(max_prob_sent[i])
    #print(max_prob_sent)
    #print(corrected_words)
    if max_prob == float("-inf"):
        max_prob_sent =  sentence
    return max_prob_sent,corrected_words


#this function is used when text is more than one sentence
#import the text as lists of list of words return a list of correct words and corrected text
def correction_text(text):
    correct_words = {}
    corrected_text = []
    
    for i in range(len(text)):
        sentence,wordlist = correction(text[i])
        #print(sentence,wordlist)
        correct_words[i] = wordlist
        corrected_text.append(sentence)
    #print(correct_words)
    #print("The corrected text is:",corrected_text)
    return correct_words,corrected_text

def accuracy(hypothesis,real,wordcount):
    correct_words = 0
    #print(hypothesis)
    #print(real)
    for index in hypothesis:
        #print(index)
        #print(hypothesis[index])
        for ans in hypothesis[index]:
            try:
                for ans2 in real[index]:
                    if ans2 == ans:
                        correct_words += 1 
            except KeyError:
                correct_words = correct_words
    correct_rate = correct_words / wordcount
    print(correct_rate)
    return correct_rate



def main():
    text, errors, errornum = getlines('holbrook-tagged.dat')
    corrected_words, corrected_text = correction_text(text[:20])
    accuracy(corrected_words, errornum)
    #print(text[3])
    #correction(text[3])

if __name__ == '__main__':
    main()


# text, errors = getlines('holbrook-tagged.dat')
# findError(text)


# text, errors = getlines('holbrook-tagged.dat')
# i = 0
# for sentence in text:
#     i = i + 1
#     findError(sentence)

#     if i == 20:
#         break
