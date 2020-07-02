#!/usr/bin/env python
# coding: utf-8
__author__ = "Admin GGCS"
__copyright__ = "Copyright 2019"
__license__ = "MIT"
__version__ = "1.2.0"
__maintainer__ = "Admin GGCS"
__website__ = "ggcs.io"

# Updated on 2020-07-01

#Setup
import requests
from bs4 import BeautifulSoup
import os
import time
from urllib.parse import urljoin
import random

#Preparing an output folder
DOWNLOAD_DIR = os.path.join(".", "DOWNLOADS")
if not os.path.isdir(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

#Input the URL of thread list.
try:
    TOC_URL = input('Thread list URLs? >> ')
except Exception as exc_msg:
    print('Error!: {}'.format(exc_msg))

#Get the TOC data
r_toc = requests.get(TOC_URL)
r_toc.encoding = 'shift_jis' #Garble killer
toc_soup = BeautifulSoup(r_toc.text, "lxml")

#Input base URL of target html files
try:
    BASE_URL = input('Base URL? >> ')
except Exception as exc_msg:
    print('Error!: {}'.format(exc_msg))

#Listing the thread URLs in a string
thread_number_list = []
for i in toc_soup.find_all('a'):
    if 'l50' in i.get('href'): # Filter for 'thread' URLs.
        thread_number_list.append(i.get('href').split('/')[0]) # Remove 'l50'

# Compose full URLs and list them.
dl_list = [urljoin(BASE_URL, i) for i in thread_number_list]
print('Following URLs('+str(len(dl_list))+' threads) have been identified.')
for j in dl_list:
    print(j)

#Proceed or not?
dl_yn = input('Download the threads? (y/n) >> ').lower()

if dl_yn == "y":
    print('STARTED!')
    turtle = ""
    # Get the target pages, append to the 'outputFile'.
    for counter, target_url in enumerate(dl_list):
        try:
            response = requests.get(target_url)
            response.encoding = 'shift-jis'
            # Correct the Meta tag.
            turtle = response.text.replace('charset=Shift_JIS', 'charset=utf8')

            #For ease of file handling, separeate html files will be generated.
            #Encoding = utf-8
            output_file_name = os.path.basename(target_url)+'.html'
            output_file_path = os.path.join(DOWNLOAD_DIR, output_file_name)

            with open(output_file_path, 'w') as f2:
                f2.write(turtle)

                pause = 5 + (random.random() * 10)
                print(output_file_name, 'has been saved. (',
                      counter + 1, 'of', len(dl_list), ': Pause -', int(pause), 'sec)')

                print('To abort: Press Control + C')
                # Pause for 'pause' seconds.
                time.sleep(pause)

        except Exception as exc_msg:
            print('Error!: {}'.format(exc_msg))

        # Emergency Brake for test run 😅
        # if counter > 1: break

    print("Completed")

else: print('*** Aborted ***')

try:
    os.system('open ' + DOWNLOAD_DIR)
except Exception as exc:
    print('Error: {}'.format(exc))
