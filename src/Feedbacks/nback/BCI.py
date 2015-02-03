
# coding: utf-8

# In[41]:

import numpy as np
import random
def wordlist(dir):
    words = np.genfromtxt(dir, delimiter=',', dtype=(None), names=True)
    wordsrand = sorted(words, key=lambda k: random.random())
    for i in range(len(wordsrand)-1):
        if wordsrand[i][0]==words[i+1][0]:
            wordsrand.append(wordsrand.pop(i+1))
    return wordsrand

def fpsConvert(ms,fps):
    return int(ms*((1.0/1000.0)*fps))
    
def stimlist(dir,listlen):

    final = []


     # In[9]:

    words = np.genfromtxt(dir, delimiter=',', dtype=(None), names=True) 


    # In[30]:

    n0 = [];n1 = []; n2 = []; n3 = [];
    for i in range(len(words)):
        if words[i][2] == 0:
            n0.append(words[i])
        if words[i][2] == 1:
            n1.append(words[i])
        if words[i][2] == 2:
            n2.append(words[i])
        if words[i][2] == 3:
            n3.append(words[i])
    n0rand = sorted(n0, key=lambda k: random.random())
    n1rand = sorted(n1, key=lambda k: random.random())
    n2rand = sorted(n2, key=lambda k: random.random())
    n3rand = sorted(n3, key=lambda k: random.random())


    # In[39]:

    if min(len(n0),len(n1),len(n2),len(n3))>listlen and listlen%4:
        for i in range(listlen/4):
            final.append(n0rand[i])
            final.append(n1rand[i])
            final.append(n2rand[i])
            final.append(n3rand[i])
            
        finalrand = sorted(final, key=lambda k: random.random())
    if min(len(n0),len(n1),len(n2),len(n3))>listlen and listlen%4==3:
        for i in range(listlen/4):
            final.append(n0rand[i])
            final.append(n1rand[i])
            final.append(n2rand[i])
            final.append(n3rand[i])
            
    finalrand = sorted(final, key=lambda k: random.random())
    return finalrand
