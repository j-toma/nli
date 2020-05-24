import tarfile
import os
import sys
import time
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
    #tar_name = 'arXiv_src_1005_006.tar'
    #t = time.process_time()
    ### countries specified in get_unis file
    unis = unis_in_countries()
    #elt=time.process_time() - t
    #print('make unis elapsed time:', elt)
    #total_count = 0
    #actual_count = 0
    tar = tarfile.open(tar_name)
    members = tar.getmembers()
    #print("num members:", len(members))
    ret = []
    #contents = []
    #hits = []
    #content_times = []
    #hit_times = []
    for member in members:
        if not member.isfile():
            continue
        else:
            article_id = member.name.rstrip('.gz')[5:]
        #print('member.name:', member.name)
        #total_count += 1
        f = tar.extractfile(member)
        #gf = gzip.open(f)
        # only .gz can be read, must ignore .pdf's
        try: 
            
            #t = time.process_time()
            unis_without_country = [ el[1] for el in unis ]
            hit = get_uni(f,unis_without_country)
            #elt=time.process_time() - t
            #hit_times.append(elt)
            if hit:
            #print('get hit elapsed time:', elt)
                #print(member.name,'has hit')
                #t = time.process_time()
                content = get_content(f)
                #elt=time.process_time() - t
                #content_times.append(elt)
                if content:
                #print(member.name,'has content')
                    #contents.append(content)
                    #hits.append(hit)
                    #actual_count += 1
                    obj = {
                            'article_id': article_id,
                            'uni': hit,
                            'content': content
                            }
                    ret.append(obj)
                    #print('actual_count:', actual_count)
                    #print('uni:',hit)
                    #print('content:',content.stdout[:100])
                    #print('content:',content[:1000])
            else:
                pass
        except OSError:
            continue
        #gf.close()
        f.close()
    tar.close()
    #print('mean content time:', sum(content_times)/len(content_times))
    #print('mean hit time:', sum(hit_times)/len(hit_times))
    #print('num_hits:', len(hits))
    #print('num_contents:',len(contents))
    #return hits, contents
    return ret

def process_tars():
    tar_files = [
            'arXiv_src_1005_005.tar',
            'arXiv_src_1005_002.tar',
            'arXiv_src_1005_006.tar',
            ]
    extracted_data = []
    for tar in tar_files:
        print('tar:', tar)
        additional_data = process_tar(tar)
        print(len(additional_data))
        extracted_data = extracted_data + additional_data
    return extracted_data


#if __name__ == '__main__':
#    import gzip
#    import timeit
#    import subprocess
#    print(
#            timeit.timeit("zh_uni()",
#            setup="from __main__ import zh_uni",
#            number=1)
#        )
    
