# JPHistoryComic-downloader

> 株式会社 小学館は、新型コロナウィルス感染症拡大による休校要請を受け、家庭学習を行う小・中・高校生への自宅学習支援として、学習まんが『小学館版学習まんが 少年少女日本の歴史』（全24巻）電子版の無料公開しました。
https://prtimes.jp/main/html/rd/p/000000594.000013640.html

それらをダウンロードしPDF化して保存する Python プログラムです。

公開期間: 2020年3月11日(水)〜4月12日(日)

## 実行方法

```
$ pipenv install
$ python main.py
```

Chrome 80 系で動かすことを念頭に dependency を組んでいるので、そうでない場合は適当に Pipfile の `chromedriver-binary` のバージョンをいじるといい気がします。

## 動作確認済環境

* macOS 10.15.3
* Google Chrome 80.0.3987.132 (Official Build) (64 ビット)
* Python 3.8.1

typing を使っているので少なくとも Python 3.5 未満では動かないはず。