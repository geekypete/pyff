
# coding: utf-8

# In[41]:

import numpy as np
import random

def wordlist(listlen):

    final = []


     # In[9]:

    words = np.genfromtxt('/home/geekypete/Downloads/pyff-master/src/feedbacks/nback/StutterBehavior.csv', delimiter=',', dtype=(None), names=True) 


    # In[30]:

    n0 = [];n1 = []; n2 = []; n3 = []; ttl =[];
    for i in range(len(words)):
        if words[i][1] == 0:
            n0.append(words[i][0])
        if words[i][1] == 1:
            n1.append(words[i][0])
        if words[i][1] == 2:
            n2.append(words[i][0])
        if words[i][1] == 3:
            n3.append(words[i][0])
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
    for i in range(len(finalrand)):
        ttl.append([finalrand[i],i+10])
    #print ttl[1][1]
    return ttl