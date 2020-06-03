import pandas as pd
from sklearn import metrics
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import Normalizer, LabelEncoder
from sklearn.calibration import CalibratedClassifierCV
from sklearn.svm import LinearSVC
from sklearn.utils import resample
import re
import time

#CLASS_LABELS = ['GB', 'US', 'CN', 'IN']
#CLASS_LABELS = ['CN', 'GB', 'IN', 'US']
CLASS_LABELS = ['NON', 'NAT']

df = pd.read_pickle('data/ds1.pickle')

#native_d = { el[1]:el[0] for el in native() }
#df.loc[:,'native'] = df['uni'].map(native_d)

#print('num train gb:', df[df.country == 'GB'].shape[0])
#print('num train us:', df[df.country == 'US'].shape[0])
#print('num train cn:', df[df.country == 'CN'].shape[0])
#print('num train in:', df[df.country == 'IN'].shape[0])
#
print('num train non native:', df[df.native == False].shape[0])
print('num train native:', df[df.native == True].shape[0])

df_maj = df[df.native==True]
df_min = df[df.native==False]

df_maj_under = resample(df_maj, replace=False, n_samples=df_min.shape[0],
        random_state=123)

df_under = pd.concat([df_min, df_maj_under])
print('under_sampled:', df_under.native.value_counts())

len_content = df_under.content.apply(lambda x:len(x)).mean()
print('len content before:', len_content)
df_under.content = df_under.content.str[:30000]
len_content = df_under.content.apply(lambda x:len(x)).mean()
print('len content after:', len_content)

stopwords = set()
stopwords.add('of china')
stopwords.add('science foundation')
stopwords.add('national natural')

def preprocess(x):
    x = re.sub('[^a-z\s]', '', x.lower())                  # get rid of noise
    x = [w for w in x.split() if w not in set(stopwords)]  # remove stopwords
    return ' '.join(x)                                     # join the list
df_under.content = df_under.content.apply(preprocess)

#X = df.content
X = df_under.content
#y = df.country
y = df_under.native
#print(y[:20])

print("Vectorizing...")
#vectorizer = CountVectorizer(analyzer='word')
vectorizer = TfidfVectorizer(ngram_range=(2,5), analyzer="word", binary=True)
#vectorizer = TfidfVectorizer(ngram_range=(2,8), analyzer="char", binary=True)
# char ngram takes forever (would need to shorted to do this realistically)
X_transformed = vectorizer.fit_transform(X)
print("Vectorization complete")

target_enc = LabelEncoder()
y = target_enc.fit_transform(y)

#print(y[:20])

X_train, X_test, y_train, y_test = train_test_split(X_transformed, y,
        test_size=0.2, random_state=7)

#normalizer = Normalizer()
#X_train = normalizer.fit_transform(X_train)
#X_test = normalizer.fit_transform(X_test)

lsvc = LinearSVC(multi_class='crammer_singer')
clf = LinearSVC(multi_class='crammer_singer')
#clf = CalibratedClassifierCV(lsvc)

s = time.time()
print("Training LinearSVC...")
#lsvc.fit(X_train, y_train)
clf.fit(X_train, y_train)
print("Training Time" + str(time.time() -s ))
s= time.time()
#print("Predicting...")
print("Linear SVC Score- "+ str(clf.score(X_test, y_test)))
#print("Predicting Time" + str(time.time() -s ))

def pretty_print_cm(cm, class_labels):
    row_format = "{:>5}" * (len(class_labels) + 1)
    print(row_format.format("", *class_labels))
    for l1, row in zip(class_labels, cm):
        print(row_format.format(l1, *row))

predicted = clf.predict(X_test)

print("\nConfusion Matrix:\n")
cm = metrics.confusion_matrix(y_test, predicted).tolist()
pretty_print_cm(cm, CLASS_LABELS)
print("\nClassification Results:\n")
print(metrics.classification_report(y_test, predicted, target_names=CLASS_LABELS, digits=4))

feature_names = vectorizer.get_feature_names() 
coefs_with_fns = sorted(zip(clf.coef_[0], feature_names)) 
df=pd.DataFrame(coefs_with_fns)
df.columns='coefficient','word'
df.sort_values(by='coefficient')
pd.options.display.max_rows = 50 
print(df[:50])
print(df[-50:])
