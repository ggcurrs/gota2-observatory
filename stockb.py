#!/usr/bin/env python
# coding: utf-8
__author__ = "Admin GGCS"
__copyright__ = "Copyright 2019"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Admin GGCS"
__website__ = "ggcs.io"

#Setup
import requests
import bs4
import os
import time
#import webbrowser
#import shutil
#import pandas as pd

#Preparing an output folder
OUTPUT_DIR = os.path.join(".", "MyOutputs")
if not os.path.isdir(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

#Input the URL of thread list.
try:
    TOC_URL = input('Thread list URLs? >> ')
except Exception as exc_msg:
    print('Error!: {}'.format(exc_msg))

#Get the TOC data
r_toc = requests.get(TOC_URL)
r_toc.encoding = 'sjis' #Garble killer
toc_soup = bs4.BeautifulSoup(r_toc.text, "lxml")

#Input base URL of target html files
try:
    BASE_URL = input('Base URL? >> ')
except Exception as exc_msg:
    print('Error!: {}'.format(exc_msg))

#Listing the thread URLs in a string
f = ""
for i in toc_soup.find_all('a', href=True):
    f += BASE_URL + i['href'][0:11] + '\n'

#Convert the string to a list and trim (pls. confirm the slice range)
dl_list = f.split('\n')[3:-4]
print('Following URLs('+str(len(dl_list))+' threads) have been identified.')
for j in dl_list:
    print(j)

#Proceed of not?
dl_yn = input('Download the threads? (y/n) >> ')

if dl_yn == "y":
    turtle = ""
    counter = 1
    for k in  dl_list:
        turtle = requests.get(k).text

        #For ease of file handling, separeate html files will be generated.
        #Encoding = utf-8
        outputFile = os.path.join(OUTPUT_DIR, 'outputFile_'+str(counter)+'.html')
        with open(outputFile, 'w') as f2:
            f2.write(turtle)
        time.sleep(5) # Delays for 5 seconds.
        print(k, 'has been saved. (',
              counter,'of', len(dl_list), ': Pose - 5 sec)')
        counter += 1
    print("Completed")

else: print('*** Aborted ***')
os.system('open ' + OUTPUT_DIR)
