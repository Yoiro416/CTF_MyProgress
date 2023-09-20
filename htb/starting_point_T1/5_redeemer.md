# Starting point5: Redeemer

## Task1
-p[min port num.]-[max port num]オプションを指定し広範囲のポート(Well-Known Port以外)をスキャンしなければ発見できない(オプションなしだとNot shown)ので、`nmap -p- -T5 [Target IP addr.]`で高速化したうえで全ポートを調査。T5オプションについては次の通り:[nmapのオプション-タイミングとパフォーマンス](https://nmap.org/man/ja/man-performance.html)

## Task3
In-memory databaseという、メモリ上で動作するデータベース。揮発性のあるmemory上で動作するためデータを永続的に保持する機能が実装されている  
IoTなどミリ秒単位の応答が求められる場面で広く利用されている。StackOverflowで人気のデータベース  

## Task4
`redis-cli`コマンドでredisサーバとやり取りが可能

## Task5
`redis-cli -help`  
`redis-cli -h [hostname/IP addr]`でホストを指定

## Task6
ホストを指定しサーバとの対話shellを起動、`info`で統計情報などを取得可能

## Task8
対話shellで`SELECT [index]`で指定番号のDBにアクセス可能

## Task9
対話shellで`keys *`ですべてのkeyを確認可能

## Task10
Task9で取得したkeyからvalueを取得する。keyは4つあったがflagというkeyで間違いないだろう:
`GET flag`