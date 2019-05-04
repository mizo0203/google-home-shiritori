# Google Home™ しりとりアプリ

## Overview

[Google Home](http://home.google.com/)™ や [Google アシスタント](https://assistant.google.com/)™ で使用できる **音声会話アプリ** です。  
AI を相手に音声操作で **しりとり** ができます。  
[Apache License 2.0](LICENSE) でソースコードを公開しています。

本アプリケーションは [Google App Engine](https://cloud.google.com/appengine/)™ (GAE) のスタンダード環境で動作します。  
ユーザと Google Home 間の会話内容を [Dialogflow](https://dialogflow.com)™ が **自然言語処理** を行い、  
GAE 上の本アプリケーションへ、ユーザ入力された単語を通知します。  

**Google Home <--> Google アシスタント <--> Dialogflow <--> しりとりアプリ on GAE**

ユーザ入力された単語を受信した本アプリケーションは、  
しりとりがつながるように **辞書データ**(後述) の中から適切な単語を返却します。  
Dialogflow としりとりアプリ間は JSON 文字列で HTTP 通信をします。

## Files
data : data file
tests: python test code
tool : other tools (ex. make json dict tool)

## Dictionary
本アプリケーションの辞書データ一覧です。    

### 一般名詞辞書

下記の辞書データから一般名詞を抽出 & 改変して利用しています。

[NAIST Japanese Dictionary](https://ja.osdn.net/projects/naist-jdic/) / [修正 BSD ライセンス](https://ja.osdn.net/projects/naist-jdic/docs/License.txt)  
Copyright (c) 2008, [Nara Institute of Science and Technology](http://www.naist.jp), Japan.

### ポケモン辞書

下記の全ポケモンの日本語データを改変して利用しています。

[pokemon_data](https://github.com/kotofurumiya/pokemon_data) / [ライセンスフリー](https://github.com/kotofurumiya/pokemon_data)  
[Koto Furumiya](https://github.com/kotofurumiya) 様  

### アニメ辞書

下記の GitHub で公開されている CSV ファイルを改変して利用しています。

[Anime DB](https://anilogia.github.io/animedb/) / [MIT License](https://github.com/anilogia/animedb/blob/master/LICENSE)  
Copyright (c) 2016-present [Anilogia](https://github.com/anilogia/)

### 駅名辞書

下記の CSV ファイルを改変して利用しています。

[日本全国の駅名一覧(2016年更新)](https://kujirahand.com/web-tools/eki.php) / [ライセンスフリー](https://kujirahand.com/web-tools/index.php)  
[くじらはんど](https://kujirahand.com/wiki/) 様

### 生物名辞書

下記を改変して利用しています。

[DBCLSメタ用語集](http://lifesciencedb.jp/lsdb.cgi?gg=dic) / [CC-表示2.1日本](https://creativecommons.org/licenses/by/2.1/jp/)  
© 2018 [DBCLS](http://dbcls.rois.ac.jp)  

## Font
[IPAフォント](https://ipafont.ipa.go.jp/old/ipafont/download.html)

---

* Google Home および Google アシスタントは Google LLC の商標です。
* その他、記載されている会社名、製品名、サービス名は、各社の登録商標または商標です。

© 2019 [Hayato Kubo](https://github.com/hayatedayon) / [Takanori Kondo](https://github.com/tKondoYDC) / [Satoki Mizoguchi](https://github.com/mizo0203), Licensed under the [Apache License, Version 2.0](LICENSE).
