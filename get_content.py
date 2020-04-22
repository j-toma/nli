import subprocess
import gzip


def get_start(gf):
    content_start = -1
    start_strs = [
            b'\\end{abstract}',
            b'\\Introduction}',
        ]
    for start_str in start_strs:
        gf.seek(0)
        if content_start != -1:
            break
        else:
            content_start = gf.read().find(start_str)
    return content_start

def get_end(gf):
    content_end = -1
    end_strs = [
            b'\\begin{thebibliography}',
            b'\\bibliography',
            b'\\sub{\\bf{References}}',
        ]
    for end_str in end_strs:
        gf.seek(0)
        if content_end != -1:
            break
        else:
            content_end = gf.read().find(end_str)
    return content_end

def get_content(f):
    gf = gzip.open(f)
    start = get_start(gf)
    if start != -1:
        end = get_end(gf)
        if start < end:
            size = end - start
            gf.seek(size)
            content = gf.read(size)
            detex_content = subprocess.run(
                    ['detex'],
                    input=content,
                    stdout=subprocess.PIPE
                )
            return detex_content
    return False
