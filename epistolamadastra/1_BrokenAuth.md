# メッセージを送信する際の認証機能について

## 概要

メッセージの送信はPOSTメソッドを用いて行われ、ペイロード内に次のデータを含む  

- authenticity_token
- message[dear]
- message[content]
- commit:"宇宙に送る"

ここで、authenticity_tokenはKRMN曰くCSRF対策のために入れたそうだが、これについて次のように検証した。

まずは特に何も編集せずメッセージを送信する
```note
authenticity_token=9ujt1An2EYUQh83S93GxB4Fjbvyontl6e39Ulhetv2dQLx8e4gCbXcGImZuox9bI_fwV4-Aj_WKPav5iFZJosQ&message%5Bdear%5D=nanka%27%3B--+%23&message%5Bcontent%5D=iroiro%27+&commit=%E5%AE%87%E5%AE%99%E3%81%AB%E9%80%81%E3%82%8B
```

次に、ペイロード内のauthenticity_tokenの値を"deleted"という文字列に置き換えてみる。ちなみに"deleted"はぱっと思いついた単語で意味はない  
```note
authenticity_token=deleted&message%5Bdear%5D=nanka%27%3B--+%23&message%5Bcontent%5D=iroiro%27+&commit=%E5%AE%87%E5%AE%99%E3%81%AB%E9%80%81%E3%82%8B
```
これを送信した。なおauthenticity_token以外の値は変更していない。　　
そしてページを読み込みなおすと、全く同じ投稿が一つ増えていた。

## 補足

メッセージに紐づけられた日時が2023年11月09日 12:02と表示されているのが前者の投稿、2023年11月09日 12:04と表示されているのが後者の投稿

## 訂正

header内のX-CSRF-Tokenとペイロード内のauthenticity_tokenのどちらかが正しければ(or)認証を通すので、どちらも消すと認証が通らなくなる(パスワードの補完でどっちかが消えたりする)
別に脆弱性ではありませんでした  
