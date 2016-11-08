import spacy
import re
from collections import defaultdict
import random
import os


def sv(s, wt):
    caps[wt] += 1
    if (wt == "Mr" and random.random() > 0.95):
        print(s)

caps = defaultdict(int)
with open("pride.txt") as f:
    txt = f.read()
    #chaps = re.split("CHAPTER \w+\n", txt)
    txt = re.sub("[\s,'\"]+", " ", txt)
    txt = re.sub("Mr\.", "Mr", txt)
    txt = re.sub("Mrs\.", "Mrs", txt)
    sens = re.split("[\.\?\!]",txt)
    for s in sens:
        ws = s.split()[1:]
        wt = None
        for w in ws:
            if (w[0:1].isupper()):
                if wt is None: wt = w
                else: wt = wt + " " + w
            else:
                if wt is not None:
                    sv(s, wt)
                    wt = None
        if wt is not None: sv(s, wt)

for (x,y) in sorted(caps.items(), key=lambda x: x[1]):
    if y < 5 : continue
    print(x, y)

#os.system('start test.html')
