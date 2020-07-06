import ahocorasick as ahc
import io, gzip
import subprocess
import time
from bs4 import BeautifulSoup as bs


def make_keywords():
    start_strs = [
            #'\\end{abstract}',
            'Introduction',
        ]
    end_strs = [
            '\\begin{thebibliography}',
            '\\bibliography',
            '\\sub{\\bf{References}}',
        ]
    return start_strs, end_strs

def make_automaton(kws):
    A = ahc.Automaton()
    for index, kw in enumerate(kws):
        A.add_word(kw, (index,kw))
    A.make_automaton()
    return A

def aho_corasick(text, kws):
    '''
        return example
        [(1874, (1, 'University of Massachusetts'))]
        loc, (index?, uni)
    '''
    A = make_automaton(kws)
    found_keywords = []
    for item in A.iter(text):
        #print(item)
        #print(line)
        found_keywords.append(item)
    return found_keywords

def analyze_hits(hits):
    s_strs, e_strs = make_keywords()

    start = (float('inf'),'')
    end = (0,'')
    has_start = False
    has_end = False
    for hit in hits:
        match = hit[1][1]
        #print('match:',match)
        loc = hit[0]
        #print('loc:',loc)
        if match in s_strs:
            if loc < start[0]:
                start = (loc,match)
        elif match in e_strs:
            if loc > end[0]:
                end = (loc,match)
    return start, end

def clean(content):
    '''
        input encoded content
        output cleaned str
    '''
    soup = bs(content,'lxml')
    xml_free = soup.get_text()
    return xml_free

def get_content(f):
    f.seek(0)
    s_strs, e_strs = make_keywords()
    kws = s_strs + e_strs
    text = io.TextIOWrapper(io.BufferedReader(gzip.open(f)), 
            encoding='utf8', errors='ignore').read()
    hits = aho_corasick(text, kws)
    start, end = analyze_hits(hits)
    size = end[0] - start[0]
    if size > 5000:
        content = text[start[0]:end[0]].encode()
        detex_content = subprocess.run(
                ['detex'],
                input=content,
                stdout=subprocess.PIPE
                )
        content = detex_content.stdout
        return content
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







