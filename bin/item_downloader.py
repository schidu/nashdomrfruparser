# -*- coding: utf-8 -*-
import traceback
from colorama import init
from colorama import Fore,Back
init()
from json import loads
import pycurl
import certifi
from io import BytesIO
import sys
import xlsxwriter
import argparse
import urllib
#import logging
#import logging.handlers
import multiprocessing
from lxml import html
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
import concurrent.futures as pool
import requests
from requests import Session
import jsonpath_ng.ext
from nash_dom_locators import *
INPUT_FILE_PATH  = "data\\input\\ids"
OUTPUT_FILE_PATH =  "data\\output\\1.xlsx"
MAX_AVAILIABLE_PROCESS_THREADS_1 = 4

def process_json_data(source,data_fields):
    data = []
    #trace print(":process_json_data")
    sorted_data_fields = sorted(data_fields.keys())
    for key in  sorted_data_fields:
        #print(key)
        #print(path.format(data_fields[key][0],val))
        for jsonp in data_fields[key]: # enumerate over each field,skip the first one for document type
            try:
                #trace print(index,val)
                jsonpath_expr = jsonpath_ng.ext.parse( jsonp ) #document type/field to retrieve
                #trace print(jsonpath_expr)
                list_val = [ match.value for match in jsonpath_expr.find(source) ]
                if not list_val:
                    data.append( '' )
                elif len(list_val)==1:
                    data.append (str(list_val[0]))
                else:
                    data.append( list_val )
            #log_file.write( f ,":", content.xpath(DATA_XPATH_TYPE_1.format(f) )[0])
            except AttributeError as e:
                data.append('')
            except Exception as e:
                sys.stderr.write(key+'\n')
                sys.stderr.write(traceback.format_exc()+'\n')
                continue
                #trace print(e)
    return data

def curl_query(q):
    #trace print(":curl query")
    try:
        buffer = BytesIO()
        c = pycurl.Curl()
        #initializing the request URL
        c.setopt(c.URL, q)
        #setting options for cURL transfer
        c.setopt(c.WRITEDATA, buffer)
        #setting the file name holding the certificates
        c.setopt(c.CAINFO, certifi.where())
        # perform file transfer
        c.perform()
        #trace print(":STATUS ",c.getinfo(pycurl.HTTP_CODE))
        #Ending the session and freeing the resources
        c.close()
        #retrieve the content BytesIO
        body = buffer.getvalue()
        #decoding the buffer
        #print(body.decode('utf-8'))
        return loads(body)
    except Exception as e:
        sys.stderr.write(traceback.format_exc()+'\n')
        #trace print(e)
        raise e

def downloader(item_id):
    #trace print(":downloader")
    sess = requests.Session()
    #trace print(item_id,flush=True)
    data = []
    try:
        object_dict = curl_query( API_QUERY.format(item_id) )
        data.extend (process_json_data(object_dict,DATA_OBJECT))
        #parse json data
        permit_dict = curl_query( PAGE_PERMITS_QUERY.format(item_id) )
        data.extend( process_json_data(permit_dict,DATA_PERMITS) )
        #trace print("permit_dict",permit_dict)
        documentation_dict  = curl_query ( PAGE_DOCUMENTATION_QUERY.format(item_id))
        #trace print(rdp_dict['data'][0])
        #trace print(DATA_PERMITS)
        data.extend( process_json_data(documentation_dict,DATA_DOCUMENTATION))
    except Exception as e:
        sys.stderr.write(traceback.format_exc()+'\n')
    finally:
        sess.close()
        return data

completion = 0
step = 0
overall = 0
def progress_indicator(future):
    global completion
    global step
    completion += 1
    if completion % step == 0:
        status  = str(round(completion*100/(overall),2)) + '%'
    else:
        status = ''
    x = 12
    y = 5
    #print('.', end='', flush=True)
    print("\033["+str(y)+";"+str(x)+"H"+status)


if __name__ == "__main__":
    # Optional positional argument
    #parser = argparse.ArgumentParser(description='Item realty parser')
    #parser.add_argument('--input', '-i', type=argparse.FileType('r'),default = "ids.txt",
    #                help='Input: text file with ids line by line.')
    # Optional positional argument
    #parser.add_argument(
    #    '--output', '-o', type=argparse.FileType('w'), default="data.xlsx",
    #    metavar='PATH',
    #    help='Output:  XLSX file. Will be rewritten if present')

    #args = parser.parse_args()
    #check_input = lambda filename: filename.lower().endswith(('txt'))
    #check_output = lambda filename: filename.lower().endswith(('xlsx'))
    #if not all(check_input(input_file.name) for input_file in args.inputs):
    #    sys.stderr.write('Input must be text file .txt')
    #    sys.exit(1)
    #if not all(check_output(output_file.name) for output_file in args.inputs):
    #    sys.stderr.write('Output must be .xlsx')
    #    sys.exit(1)
    #load ids
    ids = []
    try:
        with open(INPUT_FILE_PATH,'r') as file:
            ids =file.read().splitlines()
    except Exception as e:
        sys.stderr.write(traceback.format_exc()+'\n')
        print("Unable to read input file\nExitting")
        sys.exit(1)
    #trace print(":ids loaded")
    print("IDs to process:",len(ids))
    #sys.stderr = open('err.txt', 'w')
    try:
        # Create an new Excel file and add a worksheet.
        workbook = xlsxwriter.Workbook(OUTPUT_FILE_PATH)
        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': True})
        header = sorted(DATA_OBJECT.keys())+ \
                sorted(DATA_PERMITS.keys()) + \
                sorted(DATA_DOCUMENTATION.keys())
        #add table header
        for index,header_field in enumerate(header):
            worksheet.write(0,index, str(header_field),bold)
    except Exception as e:
        sys.stderr.write(traceback.format_exc()+'\n')
        print("Unable to create XLSX file.\nExitting")
        sys.exit(1)
    #trace print(":output xlsx created")
    #launch processing
    executor = ProcessPoolExecutor( max_workers=MAX_AVAILIABLE_PROCESS_THREADS_1 )
    print("Launching tasks")
    sys.stderr.write('') #create err.txt
    futures = [executor.submit(downloader, id_ ) for id_ in ids]
    #global completion
    #global step
    completion = 0
    overall  = len(ids)
    if overall <=10:
        step = 1
    elif overall <= 100:
        step =  2
    else:
        step = 5
    print("Completed: 0.00%")
    for future in futures:
        future.add_done_callback(progress_indicator)
    try:
        for row,f in enumerate(pool.as_completed(futures)):
            #trace print(":single task completed")
            #trace print(f.result(),flush=True)
            #fill in the results into table
            for  index,item in enumerate( f.result() ):
                try:
                    worksheet.write(row+1,index, str(item)) #skip the header row
                except Exception as e:
                    #trace print(e)
                    sys.stderr.write(traceback.format_exc()+'\n')
                    #sys.exit(1)
                    print("Unable to save data to XLSX\nPossible data loss")
        #close the workbook
        x = 12
        y = 5
        status = "100.00%"
        init()
        print("\033["+str(y)+";"+str(x)+"H"+status)
        print("\nSaving results")
        workbook.close()
        #trace print(":results saved")
        print("Scrapping completed")
    except Exception as e:
        #trace print(e)
        sys.stderr.write(traceback.format_exc()+'\n')
        print("Unable to process\nExitting")
        sys.exit(1)
