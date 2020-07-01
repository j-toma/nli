import tarfile
import os
import sys
import time
import pickle
from get_unis import unis_in_countries
#from get_content import get_content
from aho_get_content import get_content
from get_uni import get_uni




def process_tar(tar_name):
    '''
        input: (eg) '/path/arXiv_src_1005_006.tar'
        output: 
            array like
            [
                {
                    article_id: aritcle_id,
                    uni: article_uni,
                    content: article_content
                },
                ...
            ]
    '''
    directory = '/home/jtoma/nli/arxiv/dump'
    os.chdir(directory)

    ### countries specified in get_unis file
    unis = unis_in_countries()

    ### open file, get files in tar
    tar = tarfile.open(tar_name)
    members = tar.getmembers()

    ### initialize return value
    ret = []

    for member in members:

        ### things in tar are not .gz
        if not member.isfile():
            continue
        else:
            article_id = member.name.rstrip('.gz')[5:]

        ### extract individual paper
        f = tar.extractfile(member)

        try: 
            ### get uni associated with primary author of individual paper
            unis_without_country = [ el[1] for el in unis ]
            hit = get_uni(f,unis_without_country)

            if hit:

                ### get content of paper
                content = get_content(f)

                ### light preprocessing
                if content and type(content) == bytes:
                    content = content.decode('utf-8','ignore')
                    content = content.replace('\n','')

                    ### only append object to return if paper has uni and
                    ### content
                    obj = {
                            'article_id': article_id,
                            'uni': hit,
                            'content': content
                            }
                    ret.append(obj)
            else:
                pass
        except OSError:
            continue
        f.close()
    tar.close()
    return ret

def process_tars():
    tar_files = [
            'arXiv_src_1005_005.tar',
            'arXiv_src_1005_002.tar',
            'arXiv_src_1005_006.tar',
            'arXiv_src_1008_001.tar',
            'arXiv_src_1008_002.tar',
            'arXiv_src_1008_003.tar',
            'arXiv_src_1202_001.tar',
            'arXiv_src_1202_002.tar',
            'arXiv_src_1202_003.tar',
            'arXiv_src_1304_001.tar',
            'arXiv_src_1304_002.tar',
            'arXiv_src_1304_003.tar',
            'arXiv_src_1207_001.tar',
            'arXiv_src_1207_002.tar',
            'arXiv_src_1207_003.tar',
            'arXiv_src_1207_004.tar',
            'arXiv_src_1207_005.tar',
            'arXiv_src_1207_006.tar',
            # test 1
            'arXiv_src_0711_001.tar',
            'arXiv_src_0711_002.tar',
            'arXiv_src_0711_003.tar',
            'arXiv_src_0712_001.tar',
            'arXiv_src_0712_002.tar',
            'arXiv_src_0712_003.tar',
            'arXiv_src_0801_001.tar',
            'arXiv_src_0801_002.tar',
            'arXiv_src_0801_003.tar',
            'arXiv_src_0802_001.tar',
            'arXiv_src_0802_002.tar',
            'arXiv_src_0802_003.tar',
            'arXiv_src_0803_001.tar',
            'arXiv_src_0803_002.tar',
            'arXiv_src_0803_003.tar',
            'arXiv_src_0804_001.tar',
            'arXiv_src_0804_002.tar',
            'arXiv_src_0804_003.tar',
            'arXiv_src_0805_001.tar',
            'arXiv_src_0805_002.tar',
            'arXiv_src_0805_003.tar',
            # test 2
            #'arXiv_src_1305_001.tar',
            #'arXiv_src_1305_002.tar',
            #'arXiv_src_1305_003.tar',
            #'arXiv_src_1305_004.tar',
            #'arXiv_src_1305_005.tar',
            #'arXiv_src_1304_004.tar',
            #'arXiv_src_1304_005.tar',
            #'arXiv_src_1304_006.tar',
            #'arXiv_src_1304_007.tar',
            #'arXiv_src_1304_008.tar',
            #'arXiv_src_1304_009.tar',
            #'arXiv_src_1304_010.tar',
            #'arXiv_src_1304_011.tar',
            #'arXiv_src_1304_012.tar',
            #'arXiv_src_1303_001.tar',
            #'arXiv_src_1303_001.tar',
            #'arXiv_src_1303_002.tar',
            #'arXiv_src_1303_003.tar',
            #'arXiv_src_1303_004.tar',
            #'arXiv_src_1303_005.tar',
            #'arXiv_src_1303_006.tar',
            # text 3
            ]
    extracted_data = []
    for tar in tar_files:
        print('tar:', tar)
        additional_data = process_tar(tar)
        print(len(additional_data))
        extracted_data = extracted_data + additional_data
    return extracted_data

def add_tars(n):
    # load list already added and current dataset
    try:
        added_list, data = pickle.load(open('/home/jtoma/nli/data/source.pickle', 'rb'))
        print("Loading processed source files from pickle...")
    except (OSError, IOError) as e:
        print("Creating new files to pickle...")
        added_list = []
        data = []
    count = 0
    directory = os.fsencode('/home/jtoma/nli/arxiv/dump')
    for f in os.listdir(directory):
        if count <= n:
            if f not in added_list:
                filename = os.fsdecode(f)
                if filename.endswith('.tar'):
                    print('to add:', f)
                    try:
                        additional_data = process_tar(f)
                        added_list.append(f)
                        data = data + additional_data
                        count += 1
                    except:
                        pass
                else:
                    pass
            else:
                continue
        else:
            break
    pickle.dump([added_list, data], open('/home/jtoma/nli/data/source.pickle', 'wb'))
    print('successfully increased dataset size to:', len(added_list))
    print('current list of tars included:', added_list)
    return data



#process_tars()


#if __name__ == '__main__':
#    import gzip
#    import timeit
#    import subprocess
#    print(
#            timeit.timeit("zh_uni()",
#            setup="from __main__ import zh_uni",
#            number=1)
#        )
    
