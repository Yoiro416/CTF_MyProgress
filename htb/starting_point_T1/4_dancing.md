# Starting point4: Dancing

Windows機能についての勉強-SMB(Server Message Block)について知る  

## Task2

nmapで目標に対してスキャンを行い、microsoft-dsサービスに用いられているポート番号を回答

## Task4

smbclientコマンドのオプションとして、リストを取得するために使用可能なflagもしくはswitchとは何か？  

Ans. -L

## Task5

`smbclient -L [target IP]`で共有物のリスト取得  
passwordは空白で次に進むと、Guest/Anonymousとしてログインする

## Task6

Sharenameの末尾に$がないものは空白パスワードでアクセス可能

## Task7

`smbclient //10.129.191.13/WorkShares`で対話Shell起動.`smbclient \\\\10.129.191.13\\WorkShares`でも動く。エスケープの使用で`\\`が`/`扱いになるっぽい  
helpでコマンドのリストが見られるので必要なコマンドを見つけて実行.  
今回はget(と、あとlsとかcdみたいな基本的なやつ)。ディレクトリを移動してflag.txtを発見、`get flag.txt`でローカルのデフォルト位置にファイルをDLして閲覧
