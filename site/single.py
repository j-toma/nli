#from __future__ import unicode_literals
from joblib import load
import os
#from prompt_toolkit import print_formatted_text, HTML
#from xml.sax.saxutils import escape
#from IPython.display import Markdown, display
#import html.parser
#html_parser = html.parser.HTMLParser()
from markupsafe import Markup
import nltk
#nltk.download('punkt')
from nltk.tokenize import sent_tokenize, word_tokenize
from pathlib import Path

#clf, vectorizer = pickle.load(open('data/clf1.pickle','rb'))
model_file = Path('../data/pipe1.joblib')
pipeline = load(model_file)
clf = pipeline.named_steps.svc
vectorizer = pipeline.named_steps.tfidf


def feature_in_sentence(l, s):
    '''
        input
            list of sentences
            query
        output
            index of sentences that contain query
    '''
    return [index for index, value in enumerate(l) if s in value]

def display_list(c,v):
    feature_names = vectorizer.get_feature_names() 
    coefs_with_fns = sorted(zip(clf.coef_[0], feature_names)) 

    strong_non = coefs_with_fns[:100]
    count_strong_non = 0
    strong_non_list = []

    weak_non = coefs_with_fns[100:1000]
    count_weak_non = 0
    weak_non_list = []

    weak_nat = coefs_with_fns[-1000:-100]
    count_weak_nat = 0
    weak_nat_list = []

    strong_nat = coefs_with_fns[-100:]
    count_strong_nat = 0
    strong_nat_list = []

    sent_tokens = sent_tokenize(c)
    #print('sent tokens:', sent_tokens)
    for phrase in strong_non:
        spaced_phrase = ' ' + phrase[1] + ' '
        indices_of_occurences = feature_in_sentence(sent_tokens, spaced_phrase)
        #print('strong non indices of occurences:', indices_of_occurences)
        for i in indices_of_occurences:
            sent = sent_tokens[i]
            count_strong_non += 1
            replacement = '<span style="color:red">' + spaced_phrase + '</span>'
            sent = sent.replace(spaced_phrase, replacement)
            sent = Markup(sent)
            strong_non_list.append([i, sent, phrase[1], round(phrase[0],4)])
    for phrase in weak_non:
        spaced_phrase = ' ' + phrase[1] + ' '
        indices_of_occurences = feature_in_sentence(sent_tokens, spaced_phrase)
        for i in indices_of_occurences:
            sent = sent_tokens[i]
            count_weak_non += 1
            replacement = '<span style="color:orange">' + spaced_phrase + '</span>'
            sent = sent.replace(spaced_phrase, replacement)
            sent = Markup(sent)
            weak_non_list.append([i, sent, phrase[1], round(phrase[0],4)])
    for phrase in weak_nat:
        spaced_phrase = ' ' + phrase[1] + ' '
        indices_of_occurences = feature_in_sentence(sent_tokens, spaced_phrase)
        for i in indices_of_occurences:
            sent = sent_tokens[i]
            count_weak_nat += 1
            replacement = '<span style="color:yellowgreen">' + spaced_phrase + '</span>'
            sent = sent.replace(spaced_phrase, replacement)
            sent = Markup(sent)
            weak_nat_list.append([i, sent, phrase[1], round(phrase[0],4)])
    for phrase in strong_nat:
        spaced_phrase = ' ' + phrase[1] + ' '
        indices_of_occurences = feature_in_sentence(sent_tokens, spaced_phrase)
        for i in indices_of_occurences:
            sent = sent_tokens[i]
            count_strong_nat += 1
            replacement = '<span style="color:green">' + spaced_phrase + '</span>'
            sent = sent.replace(spaced_phrase, replacement)
            sent = Markup(sent)
            strong_nat_list.append([i, sent, phrase[1], round(phrase[0],4)])
    return [strong_nat_list, weak_nat_list, weak_non_list, strong_non_list]

def display_text(content):
    if type(content) == str:
        pass
    else:
        content = content.read().decode('utf-8')
    content_vectorized = vectorizer.transform([content])
    prediction = clf.predict(content_vectorized)
    #print('prediction:', prediction)
    proba = clf.decision_function(content_vectorized)
    proba = round(proba[0],4)
    #print('proba:', proba)
    content = display_list(content, vectorizer)
    return prediction, proba, content 

#def display(c,v):
#    '''
#        input content, vectorizer
#        output formatted content according to features of model
#    '''
#    feature_names = vectorizer.get_feature_names() 
#    #feature_names = p.named_steps.tfidf.get_feature_names() 
#    coefs_with_fns = sorted(zip(clf.coef_[0], feature_names)) 
#    
#    strong_non = coefs_with_fns[:100]
#    count_strong_non = 0
#    strong_non_list = []
#
#    weak_non = coefs_with_fns[100:2000]
#    count_weak_non = 0
#    weak_non_list = []
#
#    weak_nat = coefs_with_fns[-2000:-100]
#    count_weak_nat = 0
#    weak_nat_list = []
#
#    strong_nat = coefs_with_fns[-100:]
#    count_strong_nat = 0
#    strong_nat_list = []
#
#    #c = c.replace('\n', '')
#    #c = escape(c)
#    for phrase in strong_non:
#        spaced_phrase = ' ' + phrase[1] + ' '
#        if spaced_phrase in c:
#            count_strong_non += 1
#            replacement = '<span style="color:red">' + spaced_phrase + '</span>'
#            c = c.replace(spaced_phrase, replacement)
#            #matches = re.finditer(spaced_phrase, c)
#    for phrase in weak_non:
#        spaced_phrase = ' ' + phrase[1] + ' '
#        if spaced_phrase in c:
#            count_weak_non += 1
#            replacement = '<span style="color:orange">' + spaced_phrase + '</span>'
#            c = c.replace(spaced_phrase, replacement)
#    for phrase in weak_nat:
#        spaced_phrase = ' ' + phrase[1] + ' '
#        if spaced_phrase in c:
#            count_weak_nat += 1
#            replacement = '<span style="color:green">' + spaced_phrase + '</span>'
#            c = c.replace(spaced_phrase, replacement)
#    for phrase in strong_nat:
#        spaced_phrase = ' ' + phrase[1] + ' '
#        if spaced_phrase in c:
#            count_strong_nat += 1
#            replacement = '<span style="color:yellowgreen">' + spaced_phrase + '</span>'
#            c = c.replace(spaced_phrase, replacement)
#    print('num features strongly indicating nonnative:', count_strong_non)
#    print('num features weakly indicating nonnative:', count_weak_non)
#    print('num features weakly indicating native:', count_weak_nat)
#    print('num features strongly indicating native:', count_strong_nat)
#    return c

#def run_display(filename):
#    os.chdir('/home/jtoma/nli/data')
#    with open(filename) as f:
#        content =  f.read()
#        content_vectorized = vectorizer.transform([content])
#        prediction = clf.predict(content_vectorized)
#        print('prediction:', prediction)
#        proba = clf.decision_function(content_vectorized)
#        print('proba:', proba)
#        content = display(content, vectorizer)
#        content = Markup(content)
#        #formatted_content = display(content, vectorizer)
#        #print(formatted_content)
#        #print_formatted_text(HTML(formatted_content))
#        #display(Markdown((formatted_content)))
#        #mkdn = Markdown((formatted_content))
#        #unescaped = html_parser.unescape(formatted_content)
#
#        return prediction, proba, content 
#
#
#def display_upload(content):
#    if type(content) == str:
#        pass
#    else:
#        content = content.read().decode('utf-8')
#    content_vectorized = vectorizer.transform([content])
#    prediction = clf.predict(content_vectorized)
#    print('prediction:', prediction)
#    proba = clf.decision_function(content_vectorized)
#    print('proba:', proba)
#    content = display(content, vectorizer)
#    content = Markup(content)
#    #formatted_content = display(content, vectorizer)
#    #print(formatted_content)
#    #print_formatted_text(HTML(formatted_content))
#    #display(Markdown((formatted_content)))
#    #mkdn = Markdown((formatted_content))
#    #unescaped = html_parser.unescape(formatted_content)
#
#    #return prediction, proba, content 
#    return prediction, proba, content 
