# SuperFastPython.com
# download all files from a website sequentially
import zipfile
from os.path import join
from os.path import dirname
from os import makedirs
import sys
import traceback
from urllib.request import urlopen
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
import urllib
MAX_THREAD_WORKERS = 4
INPUT_FILE_PATH  = "..\\data\\input\\ids100.txt"
DATA_DIR = "..\\data\\output"
DOCS_DOWNLOAD_ARCHIVED = 'https://xn--80az8a.xn--d1aqf.xn--p1ai/%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B/api/object/{}/documentation/download?tab=projectDeclarations&tab=permits&tab=projectDocumentation&tab=developerReport'
#'https://xn--80az8a.xn--d1aqf.xn--p1ai/%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B/api/object/{}/documentation/download?tab=projectDeclarations&tab=permits&tab=projectDocumentation&tab=developerReport'
# load a file from a URL, returns content of downloaded file
def download_url(urlpath):
    # open a connection to the server
    print(urlpath,flush=True)
    with urlopen(urlpath) as connection:
        # read the contents of the url as bytes and return it
        print(connection.info().get_filename(),flush=True)
        return (connection.info().get_filename(), connection.read())
#generate id from input file
def get_id(input_filename):
    try:
        for line in open(input_filename,'r'):
            yield line.strip('\n')
    except Exception as e:
        sys.stderr.write(traceback.format_exc()+'\n')
        print("Unable to read input file\nExitting")
        sys.exit(1)

# save provided content to the local path
def save_file(path, data):
    # open the local file for writing
    with open(path, 'wb') as file:
        # write all provided data to the file
        file.write(data)
    with zipfile.ZipFile(path,'r') as zip_ref:
        zip_ref.extractall(dirname(path))
# download one file to a local directory
def download_docs_archive(id):
    link = DOCS_DOWNLOAD_ARCHIVED.format(id)
    print(link,flush=True)
    filepath = join(DATA_DIR,id)
    print(filepath,flush=True)
    try:
        makedirs(filepath , exist_ok=True)
        fname,data = download_url(link)
        # save to file
        #makedirs(filepath)
        save_file(join(filepath,fname), data)
    except Exception as e:
        print(e)
        filepath = None
    # return results
    return (link, filepath)

#print(list(get_id(INPUT_FILE_PATH)))

with ThreadPoolExecutor(max_workers=MAX_THREAD_WORKERS) as exe:
    # dispatch all download tasks to worker threads
    try:
        futures = [exe.submit(download_docs_archive, id) for id in get_id(INPUT_FILE_PATH)]
        # report results as they become available
        for future in as_completed(futures):
            # retrieve result
            link, outpath = future.result()
            # check for a link that was skipped
            if outpath is None:
                print(f'>skipped {link}')
            else:
                print(f'Downloaded {link} to {outpath}')
    except Exception as e:
        sys.stderr.write(traceback.format_exc()+'\n')
        print("Exception\nExitting")
        sys.exit(1)
