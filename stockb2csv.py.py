#!/usr/bin/env python
# coding: utf-8
__author__ = "Admin GGCS"
__copyright__ = "Copyright 2020"
__license__ = "MIT"
__version__ = "1.1.1"
__maintainer__ = "Admin GGCS"
__website__ = "ggcs.io"

# Updated on 2020-08-01

# BBS Threads to CSV
'''某掲示板スレッドのHTMLファイルを読み込み、内容を整理してCSVファィルに書き出すスクリプト'''

## 今回使うもの
import os
import sys
import chardet # Added on 2020-08-01
from bs4 import BeautifulSoup
import re
import pandas as pd

'''## ディレクトリの設定。整理整頓😉
1. Projectフォルダ（PROJECT_ROOT_PATH）を聞かれるので、フルパスを入力する。Current Directoryで良いなら "." を入力すればOK。
2. Projectフォルダの下に "source" というフォルダができるので、分析したいHTMLファイルを全部ここに入れておく（それ以外のファイルは置いちゃダメ）。
3. Projectフォルダの下に "output"というフォルダがつくれる。出来上がりのCSVファイルはここに蓄積される。
'''

# Directory set up
my_project_root_path = input('PROJECT_ROOT_PATH = ? >>  ')

PROJECT_ROOT_PATH = my_project_root_path
SOURCE_PATH = os.path.join(PROJECT_ROOT_PATH, 'source')
OUTPUT_PATH = os.path.join(PROJECT_ROOT_PATH, 'output')

if not os.path.isdir(SOURCE_PATH):
    os.makedirs(SOURCE_PATH)
if not os.path.isdir(OUTPUT_PATH):
    os.makedirs(OUTPUT_PATH)

# Confirmation:
print('Project Root path: ', PROJECT_ROOT_PATH)
print('Source path      : ', SOURCE_PATH)
print('Output Path      : ', OUTPUT_PATH)



"""## 本体部分
1. 対象となるHTMLファイルの置き場所（target_html_path）を与えると、CSVファィルに整理して、
2. output フォルダに書き出す。
"""

# Preparation:
print('\n*** HTMLファイル準備状況の確認 ***')
prep = input('HTMLファイルはsourceフォルダに準備されていますか？[Y]/N) >>  ').lower()
if not (prep == 'n' or prep == 'no'):
  source_list = os.listdir(SOURCE_PATH) # Your source files have been listed.
else:
  sys.exit('*** Aborted ***')

# Set HTML encoding.
## 某掲示板の場合、chardet だと正解の確率が低いので、お手数ですが手動で設定してください。
print('\n*** Encodingの確認 ***')
print('''HTML ファイルを、
  1: と、ある方法で用意した場合は1を選択;
  2: ブラウザで「ページを保存」した場合は2を選択;
  3: 上記でダメだった場合は3を選択;
それでもダメだった場合は、諦めてください 😭
''')
my_encoding = input('''
HTML Encoding [1, 2, 3]?
  1: UTF8
  2: Shift JIS
  3: CP932\n
>> ''')

if my_encoding == '1':
    my_enc = 'utf_8'
elif my_encoding == '2':
    my_enc = 'shift_jis'
elif my_encoding == '3':
    my_enc = 'cp932'
else:
    sys.exit('Please try again')

'''
*************
  CORE PART
*************'''
def thread_to_csv(target_html_path):
  '''Convert a bbs thread to a CSV file'''
  # Version 1.0.0 で考慮していなかった encoding の違いを吸収。
  with open(target_html_path, encoding = my_enc) as f:
    soup = BeautifulSoup(f, 'lxml')

  # Preparation:
  thread_title = soup.select('h1')[0].text
  post_list = soup.select('div.post')
  df = pd.DataFrame(columns = ['TITLE', 'POST#', 'NAME',
                               'DATE&TIME_JST', 'ID', 'MESSAGE'])
  # Extract contents from each post and clean the data:
  for i, post in enumerate(post_list):
    # Extact contents
    post_number  = post.select('span.number')[0].text # Reply Number
    post_name    = post.select('span.name')[0].text   # Name
    post_date    = post.select('span.date')[0].text   # Date and Time
    post_uid     = post.select('span.uid')[0].text    # ID
    post_message = post.select('div.message')[0].text # Message content

    # Data cleansing
    ## Format the DATE&TIME_JST strings.
    p = re.compile(r'(\d{4})/(\d{2})/(\d{2})\(.\) (\d{2}:\d{2}:\d{2}.\d{2})')
    post_date = p.sub(r'\1-\2-\3T\g<4>0', post_date)


    # Store the contents in a data frame.
    cf = pd.DataFrame([None, post_number, post_name,
                       post_date, post_uid, post_message]).T
    cf.columns = ['TITLE', 'POST#', 'NAME', 'DATE&TIME_JST', 'ID', 'MESSAGE']
    df = df.append(cf)

  # Brush up the dataframe
  df['TITLE'] = thread_title
  df.reset_index(drop=True, inplace=True)

  ## Want to drop rows where 'ID' like 'Thread'
  ### Where are they?
  #df.loc[df['ID'] == 'Thread']
  ### Their index numbers are:
  #df.loc[df['ID'] == 'Thread'].index
  ## Then drop them!
  ## Version 1.0.0 では余計な 'index=' が残っていました済みません🙇‍♂️
  df.drop(df.loc[df['ID'] == 'Thread'].index, inplace=True)

  # Output to a CSV file.
  output_file_name = os.path.basename(target_html).replace('html', 'csv')
  output_file_path = os.path.join(OUTPUT_PATH, output_file_name)
  df.to_csv(output_file_path, index = None)

  print(output_file_name, ': DONE')

if __name__ == '__main__':
  for target_html in source_list:
    thread_to_csv(os.path.join(SOURCE_PATH, target_html))
