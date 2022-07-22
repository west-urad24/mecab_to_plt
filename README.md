_mecab_to_plt.py_  
①URLを指定し、スクレイピングする。  
②名詞を抽出し、出現頻度順に並べる。  
③結果をmatplotlibに表示、横の棒グラフにする。  
※URLと取得したい件数、13行目のid,classは各自で変更して下さい。

_keyword_search_word2mecab2plot.py_  
①単語をgoogleで検索して、サイトN件取得する。  
②soupでサイトのpタグを抽出し、結果を形態素解析する。  
③品詞の上位N件取得。結果をmatplotlibに表示。
