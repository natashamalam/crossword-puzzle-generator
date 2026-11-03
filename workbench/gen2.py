from crossword.data import Entry
from crossword.grid import generate
def gen2(words,size,seed,need):
    return generate([Entry(w,"x","c") for w in words],size,seed,need,True)
