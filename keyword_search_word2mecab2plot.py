#単語をgoogleで検索して、サイトN件取得する。サイトのpタグを抽出し、結果を形態素解析する。
#品詞の上位N件取得。結果をmatplotlibに表示。

#例
# キーワード入力 SPY×FAMILY  最新刊
# 記事を何件検索したい？ 10
# 結果を上位何位まで表示したい？ 20
#
#  単語  出現回数
# ない 	 21
# 高い 	 6
# 早く 	 4
# 大きく 	 4
# 面白い 	 2
# 強く 	 2
# おもしろい 	 2
# 危うい 	 2
# しゃーない 	 2
# かわいい 	 2
# 欲しい 	 2
# いい 	 2
# 悪い 	 2
# 強 	 2
# なかっ 	 2
# すごい 	 2
# 高く 	 2
# なく 	 2
# こよなく 	 2
# 深 	 2

import MeCab,re,time,requests,bs4
from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_binary
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.support.ui import WebDriverWait

#googleで検索する文字
search_word = input('キーワード入力 ')
search_num = int(input('記事を何件検索したい？ '))
search_ranking = int(input('結果を上位何位まで表示したい？ '))#抽出し、形態素解析したときの結果

INTERVAL = 3
URL = "https://www.google.com/"
driver_path = '/Users/(My User Name))/Downloads/chromedriver'

options = Options()
options.add_argument('--headless')#ヘッドレスモード

chrome_service = fs.Service(executable_path=driver_path)
driver = webdriver.Chrome(service = chrome_service,options=options)

driver.maximize_window()
time.sleep(INTERVAL)

driver.get(URL)
time.sleep(INTERVAL)

#文字を入力して検索
driver.find_element(By.NAME, 'q').send_keys(search_word)
driver.find_elements(By.NAME,'btnK')[1].click() #btnKが2つあるので、その内の後の方、検索ボタンを押す
time.sleep(INTERVAL)

#検索結果の一覧を取得する
texts = []
results = []
flag = False
while True:
  g_list = driver.find_elements(By.CLASS_NAME,'g')
  for g in g_list:
      result = g.find_element(By.CLASS_NAME,'yuRUbf').find_element(By.TAG_NAME,'a').get_attribute('href')
      results.append(result)
      if(len(results) >= search_num):
          flag = True
          break
  if flag:
    break
  driver.find_element(By.ID,'pnnext').click() # ページ送りをクリックして次のページに移動
  time.sleep(INTERVAL)
driver.close() # 最後の行に移動

true_results = set(results)#重複をなくす
for true_result in true_results:
    res = requests.get(true_result)#重複なしURL取得
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, "html.parser")#テキストを取得
    pre_text = soup.find_all("p")
    text = re.sub("[0-9a-zA-Z]"," ", str(pre_text))#英数字を正規化
    texts.append(text)

tagger = MeCab.Tagger()
word_count = {}

for line in tagger.parse(str(texts)).splitlines():
    spl = line.split(',')#単語 \t 品詞,~,~,~
    if '形容詞' in spl[0]:
        words = spl[0].split('\t')#単語(0)、名詞、動詞(1)に分ける
        for word in words:
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1

term_list = []
count_list = []

#集計した単語の,出現回数を出力
for term, count in sorted(word_count.items(),key=lambda x:x[1], reverse=True):#降順にソート
    if(term != '形容詞'):
        #print(term,'\t',count)
        term_list.append(term)
        count_list.append(count)

#上位N件の単語と件数を表示
term_list = term_list[:search_ranking]
count_list = count_list[:search_ranking]
print('\n','単語  出現回数')

for term, count in zip(term_list, count_list):
    print(term, '\t', count)

for term, count in zip(term_list, count_list):
    print(term, '\t', count)

import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Hiragino Sans'

plt.barh(term_list, count_list) # 横棒の棒グラフ
ticks = [*range(0, (max(count_list)//10+1)*10+1, 5)]
plt.xticks(ticks, [*map(str, ticks)])
plt.savefig('result.png')
plt.show()
