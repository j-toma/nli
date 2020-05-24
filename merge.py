import pandas as pd
import glob
from process import process_tars
from get_unis import unis_in_countries

def merge():
#tar_name = 'arXiv_src_1005_006.tar'

    print('running merge')
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
    
    print('length before drop', len(df_all))
    
    additional_data = process_tars()
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
    
    print('length after drop', len(df_hit))
    print('df_hit.head():', df_hit.head())
    return df_hit

#merge()


