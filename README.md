# gota2-observatory

## Population of India
### world_population.ipynb

## PDF to CSV Project
### pdf_to_csv_prep.ipynb
Python の module, tabula と Pandas を利用して、在インド日本国大使館が公表している[インド進出日系企業リスト-2018](https://www.in.emb-japan.go.jp/Japanese/Japanese_companies_2018.html)の PDF から表のデータを抽出して CSV 化するスクリプトです。

Web site: [Google Colab: PDF to CSV 変換器を Colab に設置 [第二話 死闘篇] – NaN は dtype: float で捕捉！](https://ggcs.io/2020/08/11/google-colab-pdf-export-02/)

### pdf_to_csv_sort.ipynb
pdf_to_csv_prep.ipynb で作った DataFrame の cleansing. Pandas の pandas.Categorical() を利用します。

Web site: [Google Colab: PDF to CSV 変換器をColabに設置 [第三話 乱麻篇] – Categorical data は頼れる味方](https://ggcs.io/2020/08/19/google-colab-pdf-export-03/)

### pdf_to_csv_norm.ipynb
上の 2 つのスクリプトを使って得た df_sorted_intermed.csv を読み込んで、table_master.csv と table_biz_types.csv を出力するスクリプトです。

Web site: [Google Colab: PDF to CSV 変換器を Colab に設置 [第四話 望郷篇] – Pandas を SQL っぽく使う](https://ggcs.io/2020/08/26/google-colab-pdf-export-04/)


## stockb.py
某掲示板の某板のスクレイピング実験用のスクリプトです。

0 起動すると、カレントディレクトリの下に"DownloadedHtml"ディレクトリ（フォルダ）が生成されます。

1 最初にスレッド一覧の所在を聞かれます（"Thread list URLs?"）ので、 "https://example.com/foo/bar.html" のような形式で入力してください。全スレッドhtmlのURL一覧が表示されるので、状況を確認してください。

2 次に、各スレッドのhtmlが格納されているディレクトリを聞かれます（"Base URL?"）ので、これも "http://example.com/baz/qux/" のような感じで入力してください（最後は"/"。ここはわざと曖昧に書いてあるので、実際のサイトを見て工夫してください）。

3 スレッドの所在一覧が表示されますので、良さそうだったら"y"を入力してください。

4 ADSL環境で、300スレッド程度（全部で大体60 MBぐらい）のダウンロードが約30分で完了し、格納先の"DownloadedHtml"フォルダが開きます。

5 後は煮るなり焼くなり。なお、htmlのencodingはUTF-8です。ブラウザによっては自動判別だと文字化けするので、その場合は手動でUTF-8に設定してください。

6 設定をいじるとダウンロード速度を上げることができますが、相手のサーバに負担を掛けてしまうので自粛してください。うっかりすると新聞沙汰になって一躍有名人になれるかもしれないので、くれぐれも良識ある行動をお願いします。


## stockb2csv.py
stockb.pyでダウンロードしたhtmlファイルをパースしてCSVに整理して書き込みます。


0 起動すると、カレントディレクトリの下に、"DownloadedHtml"と"Converted"のふたつディレクトリ（フォルダ）が生成されます。（既に存在している場合作らない）
- 対象となるHTMLファイルは"DownloadedHtml"フォルダに格納されている前提。

- ファイルネームは"DownloadedHtml_[number].html"の形式を想定。

1 変換するファイル数を入力します。

2 csvに変換されたファイルは"Converted"に格納され、同フォルダが開きます。


## stockb_20070602-20190813.csv
- インターネットの巨大掲示板の「株個別銘柄(仮)」板の2007年06月02日〜2019月08月13日の書き込み（dat落ちしたものを除く。）を整理したCSVファイルです。
- 分析用のデータですので、メッセージ本体のデータは9文字目以降削除してあります。これだけでも銘柄ごとの書き込み速度は分析できます。
- 87,348行、14 MB、encoding = UTF-8、BOM無しのデータです。


## wikipedia-table.ipynb
- ある特定のWikipediaページの表を抽出するスクリプト（Jupyter Notebook用）です。
- TARGET_URLのほか、firstBlockStarts, secondBlockStarts, thirdBlockStarts, blockEndsなどのパラメータを変更して使えばそれなりに汎用性があります。
- CSVファイルで出力した場合、encoding = UTF-8、BOM無しとなるので、Excelから開く場合はencodingを手動で設定してください。


## jiroCalc-01.ipynb
- 日本食品標準成分表のデータからラーメン二郎のカロリー 、成分を計算するスクリプト（Jupyter Notebook用）です。
- Sample data は https://github.com/ggcurrs/data/blob/master/jiro-nutrition-facts.csv です。
