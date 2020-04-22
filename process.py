import tarfile
import os
import sys
import time
from get_unis import unis_in_countries
#from get_content import get_content
from aho_get_content import get_content
from get_uni import get_uni

def zh_uni():
    directory = '/home/jtoma/nli/arxiv/dump'
    os.chdir(directory)
    tar_name = 'arXiv_src_1005_006.tar'
    t = time.process_time()
    unis = unis_in_countries(['CN','GB','US','IN'])
    elt=time.process_time() - t
    print('make unis elapsed time:', elt)
    total_count = 0
    actual_count = 0
    tar = tarfile.open(tar_name)
    members = tar.getmembers()
    print("num members:", len(members))
    contents = []
    hits = []
    content_times = []
    hit_times = []
    for member in members:
        if not member.isfile():
            continue
        #print('member.name:', member.name)
        total_count += 1
        f = tar.extractfile(member)
        #gf = gzip.open(f)
        # only .gz can be read, must ignore .pdf's
        try: 
            
            t = time.process_time()
            hit = get_uni(f,unis)
            elt=time.process_time() - t
            hit_times.append(elt)
            if hit:
            #print('get hit elapsed time:', elt)
                #print(member.name,'has hit')
                t = time.process_time()
                content = get_content(f)
                elt=time.process_time() - t
                content_times.append(elt)
                if content:
                #print(member.name,'has content')
                    contents.append(content)
                    hits.append(hit)
                    actual_count += 1
                    print('actual_count:', actual_count)
                    print('uni:',hit)
                    print('content:',content.stdout[:100])
            else:
                pass
        except OSError:
            continue
        #gf.close()
        f.close()
    tar.close()
    print('mean content time:', sum(content_times)/len(content_times))
    print('mean hit time:', sum(hit_times)/len(hit_times))
    print('num_hits:', len(hits))
    print('num_contents:',len(contents))
    return hits, contents

if __name__ == '__main__':
    import gzip
    import timeit
    import subprocess
    print(
            timeit.timeit("zh_uni()",
            setup="from __main__ import zh_uni",
            number=1)
        )
    
