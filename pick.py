from collections import OrderedDict
import random
import re
books = ['emma','mansfield','northanger','persuasion','sense','susan']
#'pride',

pbooks = list()

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
        self.sentences = re.split("[\.\?\!]",txt)

class Book:
    def __init__(self, name, file):
        self.name = name
        self.file = file
        self.volumes = list()
    def add_volume(self, n):
        v = Volume(n)
        self.volumes.append(v)
        return v
    def random(self):
        return random.choice(self.volumes)

for bn in books:
    b = Book(bn, bn+".txt")
    with open(b.file) as f:
        lineno = 0
        v = None
        c = None
        p = None
        for l in f:
            lineno += 1
            if l.upper().startswith("VOLUME"):
                if p is not None: p.close()
                v = b.add_volume(l[7:].strip())
                #print("---",v.name, lineno)
                continue
            if l.upper().startswith("CHAPTER"):
                if v is None:
                    v = b.add_volume("I")
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
    if len(b.volumes) == 0: continue
    pbooks.append(b)

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
    
