import pandas as pd
from sklearn import metrics
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import Normalizer, LabelEncoder
from sklearn.calibration import CalibratedClassifierCV
from sklearn.svm import LinearSVC, SVC
from sklearn.utils import resample
from sklearn.feature_selection import SelectFromModel, SelectKBest, SelectPercentile, chi2, mutual_info_classif
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from joblib import dump
import re
import time


def pretty_print_cm(cm, class_labels):
    row_format = "{:>5}" * (len(class_labels) + 1)
    print(row_format.format("", *class_labels))
    for l1, row in zip(class_labels, cm):
        print(row_format.format(l1, *row))

def remove_bigram_stops(doc):
    doc = re.sub('[^a-z\s]', '', doc.lower())                  # get rid of noise
    stop_phrases = [
    # note: this regex considers "... red. Roses..." as fair game for removal.
    #       if that's not what you want, just use ["red roses"] instead.
            "of(\s?\\.?\s?)china",
            "national(\s?\\.?\s?)natural",
            "science(\s?\\.?\s?)foundation",
            "eqnarray",
            "et al.",
            ]
    for phrase in stop_phrases:
        doc = re.sub(phrase, "", doc, flags=re.IGNORECASE)
    return doc

def under_sample(df):
    print('Original counts:')
    print('non native:', df[df.native == False].shape[0], '| native:', df[df.native == True].shape[0])
    
    df_maj = df[df.native==True]
    df_min = df[df.native==False]
    
    df_maj_under = resample(df_maj, replace=False, n_samples=df_min.shape[0],
            random_state=123)
    
    df_under = pd.concat([df_min, df_maj_under])

    print('count of native after resample:', df_under.native.value_counts()[0])
    print('----')

    return df_under

def filter_categories(df):

    # only cs and not physics
    df1 = df[df['categories'].str.contains('cs.') & ~(df['categories'].str.contains('ics.'))]

    # cs, economics, quantitative finance
    #df1 = df[df['categories'].str.contains('cs.')
            #| df['categories'].str.contains('econ.')
            #| df['categories'].str.contains('q-fin.')
    #        ]
    return df1

def cut_content(df):
    mean_len_content_before = df.content.apply(lambda x:len(x)).mean()
    df.content = df.content.str[:20000]
    mean_len_content_after = df.content.apply(lambda x:len(x)).mean()
    print('Average character count in content:')
    print('before cut:', mean_len_content_before, '| after cut:',
            mean_len_content_after)
    print('----')
    return df

def get_fn_fp(df, predicted, y_test):
    count_fn, count_fp  = 0, 0
    fp_list, fn_list= [], []
    for row_index, (prediction, label) in enumerate(zip (predicted, y_test)):
        if prediction != label:
            df_index = y_test.index.tolist()[row_index]
            if label:
                count_fn += 1
                fn_list.append(df_index)
            else:
                count_fp += 1
                fp_list.append(df_index)
            #print('Row', row_index, 'has been classified as', prediction, 'and should be', label)
    #print('num FN:', count_fn)
    #print('FN list:', fn_list)
    #print('num FP:', count_fp)
    #print('FP list:', fp_list)
    return list(df.loc[fn_list]['arxiv_id']), list(df.loc[fp_list]['arxiv_id'])


def run():
    #CLASS_LABELS = ['CN', 'GB', 'IN', 'US']
    CLASS_LABELS = ['NON', 'NAT']
    
    # get data
    df = pd.read_pickle('data/ds1.pickle')

    # filter categories
    df = filter_categories(df)
    
    # unkdersample majority class to size of minority
    df_under = under_sample(df)
    #print('Original counts:')
    #print('non native:', df[df.native == False].shape[0], '| native:', df[df.native == True].shape[0])
    #df_under = df
    
    # trim content length for faster training
    #df_under = cut_content(df_under)
    
    # remove nonlinguistic indicators
    df_under.content = df_under.content.apply(remove_bigram_stops)

    # retain ids 
    #df_under.set_index('arxiv_id', inplace=True)

    # set data
    X = df_under.content
    y = df_under.native
    print('length of X:', len(X))
    
    clf = Pipeline(
            steps=[
                ('tfidf', TfidfVectorizer(ngram_range=(2,3), analyzer='word',
                    binary=True, max_features=5000)),
                ('svc', LinearSVC(multi_class='crammer_singer',
                    class_weight='balanced')),
            ]
    )


    
    # if using multiclass need to encode labels
    #target_enc = LabelEncoder()
    #y = target_enc.fit_transform(y)
    

    #X_train, X_test, y_train, y_test = train_test_split(X_transformed, y,
    X_train, X_test, y_train, y_test = train_test_split(X, y,
            test_size=0.2, random_state=7)
    
    print('length of X_train:', len(X_train))
    print('length of X_test:', len(X_test))
    
    s = time.time()
    print("Training LinearSVC...")
    clf.fit(X_train, y_train)
    print("Training Time" + str(time.time() -s ))
    s= time.time()
    print("Linear SVC Score- "+ str(clf.score(X_test, y_test)))
    print('----')
    
    
    predicted = clf.predict(X_test)

    fn, fp = get_fn_fp(df_under, predicted, y_test)
    print('false negatives:', fn)
    print('false positives:', fp)

    print('Results')
    print("\nConfusion Matrix:\n")
    cm = metrics.confusion_matrix(y_test, predicted).tolist()
    pretty_print_cm(cm, CLASS_LABELS)
    print("\nClassification Results:\n")
    print(metrics.classification_report(y_test, predicted, target_names=CLASS_LABELS, digits=4))
    #
    dump(clf, 'data/pipe1.joblib')
    print('pipeline dumped to pipe1.joblib')

    #feature_names = clf.named_steps.tfidf.get_feature_names() 
    # if using calibratedclassifierCV
    #coef_avg = 0
    #for i in clf.calibrated_classifiers_:
    #    coef_avg = coef_avg + i.base_estimator.coef_
    #coef_avg  = coef_avg/len(clf.calibrated_classifiers_)
    #coefs_with_fns = sorted(zip(coef_avg, feature_names)) 

    #coefs_with_fns = sorted(zip(clf.named_steps.svc.coef_[0], feature_names)) 
    #df=pd.DataFrame(coefs_with_fns)
    #df.columns='coefficient','n-gram'
    #df.sort_values(by='coefficient')
    #pd.options.display.max_rows = 50 
    #print('top 50 ngrams indicating non native:')
    #print(df[:50])
    #print('top 50 ngrams indicating native:')
    #print(df[-50:])
    #print('----')
    #pickle.dump([clf, vectorizer], open('data/clf1.pickle', 'wb'))
    #print('classifier, vectorizer, and features dumped to pickle clf1.pickle')
    print('run completed')

run()
    

