#!/usr/bin/env python
# coding: utf-8
__author__ = "Admin GGCS"
__copyright__ = "Copyright 2019"
__license__ = "MIT"
__version__ = "1.0.1e"
__maintainer__ = "Admin GGCS"
__website__ = "ggcs.io"

import os
import requests
from bs4 import BeautifulSoup
#import webbrowser
#import shutil
import numpy as np
import pandas as pd

"""
カレントディレクトリの下に、"DownloadedHtml"と"Converted"のふたつのフォルダを作る。
（既に存在している場合作らない）
- 対象となるHTMLファイルは"DownloadedHtml"フォルダに格納されている前提。
- ファイルネームは"DownloadedHtml_[number].html"の形式を想定。
- csvに変換されたファイルは"Converted"フォルダに作られる。
"""

SOURCE_DIR = os.path.join(".", "DownloadedHtml")
if not os.path.isdir(SOURCE_DIR):
    os.makedirs(SOURCE_DIR)

OUTPUT_DIR = os.path.join(".", "Converted")
if not os.path.isdir(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)


#変換するファイルの数を入力
try:
    fileNumber = input('Number of files? >> ')
except Exception as exc_msg:
    print('Error!: {}'.format(exc_msg))

#ファイル変換
for i in range(int(fileNumber)):
    sourceHtml = os.path.join(SOURCE_DIR, 'DownloadedHtml_'+str(i+1)+'.html')
    with open(sourceHtml) as htmlFile:
        soup = BeautifulSoup(htmlFile, features="lxml")

    #項目データの取り出し。
    title = (soup.find_all('title')[0].getText())[0:-3] #このスライスは適宜設定
    listNumber = soup.find_all('span', 'number')
    listName = soup.find_all('span', 'name')
    listDate= soup.find_all('span', 'date')
    listUid= soup.find_all('span', 'uid')
    listMsg= soup.find_all('div', 'message')

    #getText()でタグを取り除く。いきなりDataFrameに書き込むとタグ取りがやり難いのでlist typeを経由。
    listWhole = []
    for j in range(len(listNumber)):
        listWhole += [
            [title, listNumber[j].getText(), listName[j].getText(), listDate[j].getText(),
            listUid[j].getText(), listMsg[j].getText()]]

    df = pd.DataFrame(listWhole, columns=['Title', 'Number', 'Name', 'Date', 'ID', 'Msg'])
    outputCsv = os.path.join(OUTPUT_DIR, 'Conv_'+str(i+1)+'.csv')
    df.to_csv(outputCsv, index=False)

print('Done! 🍻')
os.system('open '+ OUTPUT_DIR)
