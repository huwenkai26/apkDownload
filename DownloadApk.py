from gevent import monkey

monkey.patch_all()
from gevent.pool import Pool
import requests
import sys
import os


def download(url,filename):
    chrome = 'Mozilla/5.0 (X11; Linux i86_64) AppleWebKit/537.36 ' + '(KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'
    headers = {'User-Agent': chrome}

    filename = (url.split('/')[-1].strip())
    r = requests.get(url.strip(), headers=headers, stream=True)
    with open(filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()
    print(filename + "is ok")


def removeLine(key, filename):
    os.system('sed -i /%s/d %s' % (key, filename))


if __name__ == "__main__":

    filename = 'urls.txt'
    if len(filename) > 2:


        f = open(filename, "r")
        p = Pool(4)
        i=1

        for line in f.readlines():
            if line:
                name = str(i)+".apk"
                i+=1
                p.spawn(download, line.strip(),name)
                key = line.split('/')[-1].strip()
                removeLine(key, filename)
        f.close()
        p.join()
    else:
        print( 'Usage: python %s urls.txt' % sys.argv[0])
