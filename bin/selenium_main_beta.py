from concurrent.futures import ProcessPoolExecutor
import concurrent.futures
from functools import partial
import re
import psutil
from contextlib import suppress
from itertools import repeat
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.chrome.service import Service
#from webdriver_manager.chrome import ChromeDriverManager
from multiprocessing import Lock
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
#from webdriver_manager.core.utils import ChromeType
#from selenium.webdriver.chrome.service import Service
#from webdriver_manager.chrome import ChromeDriverManager
import time
import urllib
import subprocess
#from selenium.webdriver.firefox.options import Options
OUTPUT_FILE_PATH = "..\\data\\output\\ids"
MAX_AVAILIABLE_PROCESS_THREADS_1 = 2
PAGE_QUERY = 'https://xn--80az8a.xn--d1aqf.xn--p1ai/%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B/%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3-%D0%BD%D0%BE%D0%B2%D0%BE%D1%81%D1%82%D1%80%D0%BE%D0%B5%D0%BA/%D1%81%D0%BF%D0%B8%D1%81%D0%BE%D0%BA-%D0%BE%D0%B1%D1%8A%D0%B5%D0%BA%D1%82%D0%BE%D0%B2/%D1%81%D0%BF%D0%B8%D1%81%D0%BE%D0%BA?objStatus=0&page={}&limit=100'
PAGINATION_CSS_SELECTOR = 'ul.pagination'
MAX_PAGES_XPATH_SELECTOR = './li[last()-1]/a'
url_ids_xpath = '//*[@id="preloader"]/div[1]/div[3]/div[1]/div/div/div[2]/a'
xp = '//*[@id="preloader"]'
xxp = '//*[@id="preloader"]/div[1]/div[3]/div[2]/div/div/div/div[1]/div[1]/div[1]/div/a'

text_xp = '//span[not(contains(@style,"display:none")) and contains(text(),"ID дома:")]'
FULL_SCREEN_IDS_XPATH_SELECTOR = '//div[@id="preloader"]/div/div/div/div/div/div/a/div/div[2]/div/a/div[1]/span' #100 elements
CHROMEDRIVER_EXE_PATH = "chromedriver.exe"

def get_page(first_page=True, page_num=0):
    print( ':get_page',flush=True )
    ids = []
    try:
        options = Options()
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)
        chromedriver_processes=[]
        if get_page.driver is None:
            get_page.driver = webdriver.Chrome(executable_path=CHROMEDRIVER_EXE_PATH,options=options)
            for process in psutil.process_iter():
                if process.name() == 'chrome.exe' and '--test-type=webdriver' in process.cmdline():
                    with suppress(psutil.NoSuchProcess):
                        chromedriver_processes.append(process.pid)            #get_page.driver = driver
            #get_page.driver.set_window_position(0, 0)
            #get_page.driver.set_window_size(1024, 768)
            print( ':driver loaded',flush=True )
        query = urllib.parse.unquote(PAGE_QUERY.format(str(page_num)))
        get_page.driver.get( query )
        wait = WebDriverWait(get_page.driver,60)
        if first_page:
            wait = WebDriverWait( get_page.driver,60 )
            el = wait.until( EC.presence_of_element_located( (By.CSS_SELECTOR,PAGINATION_CSS_SELECTOR) ))
            max_page = int(el.find_element( By.XPATH,  MAX_PAGES_XPATH_SELECTOR ).get_attribute('innerHTML'))
            print(":max page:", max_page)
        el = wait.until( EC.element_to_be_clickable( (By.XPATH, FULL_SCREEN_IDS_XPATH_SELECTOR)) )
        if ( not el is None ):
            print(":ids found",flush=True)
            els = get_page.driver.find_elements( By.XPATH,  FULL_SCREEN_IDS_XPATH_SELECTOR )
            if (len(els)>0):
                print( ":ids parsed:", len(els) )
                for el in els:
                    if not el is None:
                        if len( el.text ) > 0:
                            if not re.search( "\d+", el.text ) is None: # id is a series of digits
                                ids.append( re.search( "\d+", el.text).group(0) ) #id
                print( ':done',flush=True )
    except Exception as ex:
        print("ERROR:ids not parsed",flush=True)
        print(ex,flush=True)
    finally:
        if first_page:
            get_page.driver.close()
            return (max_page,ids)
        else:
            return (tuple(chromedriver_processes),ids)

get_page.driver = None

def scrape_ids():
    max_page ,res_0 = get_page( first_page=True, page_num=str(0) )  # parse first page and get the overall number of pages
    indexes = ( page_index  for page_index in range(1,max_page) ) # generator of page URLS
    res = [] # resultant list of ids
    res.extend( res_0 ) # keep ids from first page
    #run multiple processes and wait for results
    processes = set()
    with ProcessPoolExecutor( max_workers=MAX_AVAILIABLE_PROCESS_THREADS_1 ) as executor:
        futures = [executor.submit( get_page, first_page=False, page_num=index ) for index in indexes]
        for _ in futures:
            try:
                chromedriver_processes,ids = _.result()
                processes = processes.union(set(chromedriver_processes))
                res.extend( ids ) # keep the result of each single process once done
            except Exception as e:
                print(e) # any network or memory mulfunction produces an exception
    #save results from all threads into file
    f = open(OUTPUT_FILE_PATH,"w")
    for r in res:
        #print(r)
        f.write(str(r)+'\n')
    f.close()
    kill_command = ' taskkill /PID {} /F 1>nul 2>&1'
    print(":killing chromedrivers")
    for pid in processes:
        p = subprocess.Popen(kill_command.format(str(pid)), stdout=subprocess.PIPE, shell=True)
        #one_line_output = p.stdout.readline()
        #print(one_line_output)
    print(":killed")


if __name__ == '__main__':
    scrape_ids()
