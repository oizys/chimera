from collections import OrderedDict, defaultdict
import random
import re
from itertools import takewhile, chain
books = ['emma','mansfield','northanger','persuasion','sense','susan']
#'pride',

def is_caps(x):
    return len(x) > 0 and x[0:1].isupper()

class Volume:
    def __init__(self, name):
        self.name = name
        self.chapters = list()
    def add_chapter(self, name):
        c = Chapter(name)
        self.chapters.append(c)
        return c
    def random(self):
        return random.choice(self.chapters)

class Chapter:
    def __init__(self, name):
        self.name = name
        self.paragraphs = list()
    def add_paragraph(self):
        p = Paragraph()
        self.paragraphs.append(p)
        return p
    def random(self, ml,xl):
        seq = list(filter(lambda x: len(x.lines) >= ml and len(x.lines) <= xl, self.paragraphs))
        return random.choice(seq)

class Sentence:
    def __init__(self,txt):
        self.text = txt
        self.characters = None
    def get_characters(self):
        if self.characters is not None: return self.characters
        ws = iter(self.text.split()[1:])
        o = []
        while True:
            w = next(ws, None)
            if w is None: break
            if not is_caps(w): continue
            propr = " ".join(takewhile(is_caps, ws))
            if len(propr) == 0: continue
            o.append(propr)
        self.characters = o
        return o

class Paragraph:
    def __init__(self):
        self.text = ""
        self.lines = list()
    def close(self):
        txt = "".join(self.lines)
        #txt = re.sub("[\s,'\"]+", " ", txt)
        txt = re.sub("[\s]+", " ", txt)
        txt = re.sub("Mr\.", "Mr", txt)
        txt = re.sub("Mrs\.", "Mrs", txt)
        self.text = txt
        self.sentences = [Sentence(s) for s in re.split("[\.\?\!]",txt)]
    @property
    def characters(self):
        return chain.from_iterable(s.get_characters() for s in self.sentences if len(s.get_characters()) > 0)

class Character:
    def __init__(self, name):
        self.name = name
        self.count = 0
        # locations
        # words around

class Book:
    def __init__(self, name, file):
        self.name = name
        self.file = file
        self.volumes = list()
        self.characters = dict()
    def add_volume(self, n):
        v = Volume(n)
        self.volumes.append(v)
        return v
    @property
    def chapters(self):
        return chain.from_iterable((v.chapters for v in self.volumes))
    @property
    def paragraphs(self):
        return chain.from_iterable((c.paragraphs for c in self.chapters))
    def random(self):
        return random.choice(self.volumes)
    def process(self):
        for c in chain.from_iterable(p.characters for p in self.paragraphs):
            if c not in self.characters:
                self.characters[c] = Character(c)
            self.characters[c].count += 1
            #if (random.random() < 0.01): print(c)
    def parse(self):
        with open(self.file) as f:
            lineno = 0
            v = None
            c = None
            p = None
            for l in f:
                lineno += 1
                if l.upper().startswith("VOLUME"):
                    if p is not None: p.close()
                    v = self.add_volume(l[7:].strip())
                    #print("---",v.name, lineno)
                    continue
                if l.upper().startswith("CHAPTER"):
                    if v is None:
                        v = self.add_volume("I")
                    if p is not None: p.close()
                    c = v.add_chapter(l[8:].strip())
                    #print(c.name, lineno)
                    continue
                if l == "\n":
                    if c is not None:
                        if p is not None: p.close()
                        p = c.add_paragraph()
                    continue
                if p is not None:
                    #if random.random() > 0.99: print(l)
                    p.lines.append(l)
            if p is not None: p.close()  

class Library:
    def __init__(self, books):
        self.byname = dict()
        self.books = list()
        for bn in books:
            b = Book(bn, bn+".txt")
            b.parse()
            if len(b.volumes) == 0: continue
            self.books.append(b)
            self.byname[b.name] = b
    def __str__(self):
        s = ""
        for b in self.books:
            s += b.name + "\n"
        return s


def pickfragments():
    def pck():
        b = random.choice(pbooks)
        v = b.random()
        c = v.random()
        p = c.random(3,10)
        pi = c.paragraphs.index(p)
        return [b,v,c,pi,p.text]
    picks = [pck() for x in range(1,20)]
    with open("sp.txt","w+") as of:
        with open("picks.txt","w+") as f:
            for p in picks:
                of.write(p[4]+"\n")
                f.write(p[4]+"\n\n")
                of.write(" ".join(["---------",p[0].name,p[1].name,p[2].name,str(p[3])])+"\n\n")

libr = Library(books)
emma = libr.byname["emma"]

con = 0
caps = defaultdict(int)
for cs in (p.characters for p in emma.paragraphs):
    for c in cs:
        con += 1
        caps[c] += 1
        #if (random.random() < 0.01): print(c)
        
p = emma.random().random().random(2, 4)
#print (p.text)

emma.process()

for (x,y) in sorted(emma.characters.items(), key=lambda x: x[1].count):
    if y.count < 30 : continue
    print(x, y.count)
