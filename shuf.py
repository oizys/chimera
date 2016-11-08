import random
with open("sp.txt","w") as of:
    with open("picks.txt") as f:
        lns = f.readlines()
        random.shuffle(lns)
        of.write("\n".join(lns))
    
