import pandas as pd
import glob
import pickle
import os
#from process import process_tars
from process import add_tars
from get_unis import unis_in_countries, native

def merge(n):

    STORE_PATH = '/home/jtoma/nli/data'
    f = 'metadata.pickle'
    metadata_path = os.path.join(STORE_PATH, f)
    print('running merge')
    try:
        # df_all could be renamed to metadata
        df_all = pd.read_pickle(metadata_path)
        print("Loading metadata from pickle")
    except (OSError, IOError) as e:
        print("Creating metadata pickle")
        dumpdate = "20190101"
        datadir = "arxiv_archive-1.0.1/processed_data/" + dumpdate + "/per_year/"
        
        files = glob.glob(datadir + "*.tsv.zip")
        len(files)
        files.sort()
        
        dtypes = {
            "abstract": object,
            "acm_class": object,
            "arxiv_id": object,
            "author_text": object,
            "categories": object,
            "comments": object,
            "created": object,
            "doi": object,
            "num_authors": int,
            "num_categories": int,
            "primary_cat": object,
            "title": object,
            "updated": object,
            "created_ym": object
        }
        
        df_all = pd.DataFrame()
        for f in files:
            print(f)
            yearly_df = pd.read_csv(
                    f,
                    sep="\t",
                    index_col=0,
                    compression='zip',
                    dtype=dtypes,
                    parse_dates=["created","updated"])
            df_all = df_all.append(yearly_df)
        df_all.to_pickle(metadata_path)
    
    print('length before drop', len(df_all))
    
    #additional_data = process_tars()
    # every time we run merge, we increase the size of the dataset
    additional_data = add_tars(n)

    keys = [additional_data[i]['article_id'] for i in
            range(len(additional_data))]
        
        #df = df_all.drop(df_all[df_all.arxiv_id in keys].index)
        #df = df_all[df_all.arxiv_id in keys]
        #df = df_all[df_all.arxiv_id.isin(keys)]
    is_hit = df_all['arxiv_id'].isin(keys)
    df_hit = df_all[is_hit]
    
    uni_d = { additional_data[i]['article_id']: additional_data[i]['uni'] for
            i in range(len(additional_data)) }
    #df_hit['uni'] = uni_d
    df_hit.loc[:,'uni'] = df_hit['arxiv_id'].map(uni_d)
    
    content_d = { additional_data[i]['article_id']: additional_data[i]['content'] for
            i in range(len(additional_data)) }
    #df_hit['content'] = content_d
    df_hit.loc[:,'content'] = df_hit['arxiv_id'].map(content_d)
    
    country_d = { el[1]:el[0] for el in unis_in_countries() }
    df_hit.loc[:,'country'] = df_hit['uni'].map(country_d)
    
    native_d = { el[1]:el[0] for el in native() }
    df_hit.loc[:,'native'] = df_hit['uni'].map(native_d)

    print('length after drop', len(df_hit))
    print('df_hit.head():', df_hit.head())
    STORE_PATH = '/home/jtoma/nli/data/'
    file_name = 'ds1.pickle'
    pickle_file = os.path.join(STORE_PATH, file_name)
    df_hit.to_pickle(pickle_file)
    return df_hit

merge(10)


