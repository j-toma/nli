import ahocorasick as ahc
from get_unis import unis_in_countries
import io, gzip, time


def make_automaton(unis):
    A = ahc.Automaton()
    for index, uni in enumerate(unis):
        A.add_word(uni, (index,uni))
    A.make_automaton()
    return A

def aho_corasick(text, unis):
    '''
        return example
        [(1874, (1, 'University of Massachusetts'))]
        loc, (index?, uni)
    '''
    A = make_automaton(unis)
    found_keywords = []
    for item in A.iter(text):
        #print(item)
        #print(line)
        found_keywords.append(item)
        break
    return found_keywords

def get_uni(f, unis):
    #t = time.process_time()
    f.seek(0)
    title_loc = f.read().find(b'\\title{')
    f.seek(title_loc - 2000)
    #elapsed_time = time.process_time() - t
    #print('find title elapsed:', elapsed_time)
    text = io.TextIOWrapper(io.BufferedReader(gzip.open(f)), \
            encoding='utf8', errors='ignore').read(6000)
    #elapsed_time = time.process_time() - t
    #print('read elapsed:', elapsed_time)
    hit = aho_corasick(text, unis)
    #elapsed_time = time.process_time() - t
    #print('uni aho elapsed:', elapsed_time)
    if hit:
        return hit[0][1][1]
    else:
        return False


    

#from ahocorapy.keywordtree import KeywordTree
#
#
#def build_kwtree(unis):
#    kwtree = KeywordTree()
#    for uni in unis:
#        kwtree.add(uni.encode())
#    kwtree.finalize()
#    return kwtree
#
#def find_keywords(content,unis):
#    kwtree = build_kwtree(unis)
#    hits = kwtree.search_all(content)
#    for hit in hits:
#        print(hit)







