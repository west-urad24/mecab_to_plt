#yahooの記事をn件スクレイピングし、形態素解析する
import requests,bs4,re
import MeCab
import unidic

URL = str(input('URL '))#例　https://news.yahoo.co.jp/articles/2dcc7a8bc191252476cdaa14e1cd51cc58ebcfcd
res = requests.get(URL)

res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, "html.parser")#テキストを取得

#検索
pre_text = soup.find(class_="sc-iqzUVk")#htmlのidかclassかで探す。サイトによってidかclassの文字を変える
text = re.sub('[a-z]|[A-Z]', '', str(pre_text))#英字を削除、正規化
tagger = MeCab.Tagger()
word_count = {}

for line in tagger.parse(text).splitlines():#解析した単語と瀕死を一行ずつ読み取る
    spl = line.split(',')
    if '名詞'in spl[0]:
        words = spl[0].split('\t')#単語と「名詞」に分ける
        for word in words:
            if word in word_count:#同じ単語を調べる
                word_count[word] += 1
            else:
                word_count[word] = 1

term_list = []
count_list = []

#集計した単語の,出現回数を出力
for term, count in sorted(word_count.items(),key=lambda x:x[1], reverse=True):#降順にソート
    if(term != '名詞'):#結果に「名詞」が出てこないようにする
        if(term != '代名詞'):
            #print(term,'\t',count)
            term_list.append(term)
            count_list.append(count)

#上位20件の単語と件数を表示
N = 20
term_list = term_list[:N]
count_list = count_list[:N]
print('[単語 出現回数]','\n')
for term, count in zip(term_list, count_list):
    print(term, '\t', count)

import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Hiragino Sans'

plt.barh(term_list, count_list) # 横棒の棒グラフ
ticks = [*range(0, (max(count_list)//10+1)*10+1, 5)]
plt.xticks(ticks, [*map(str, ticks)])
plt.savefig('result.png')
plt.show()
