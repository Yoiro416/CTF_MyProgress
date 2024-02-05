# Starting point Tier2 : Crocodile

# Task1

-sCオプションを与えることでNmapはデフォルトスクリプトを有効化しながらスキャンを行う

# Task2

```bash
nmap [ipaddr] -sV -p 21
```
で21番ポートのサービスを検出  
ちなみに
```bash
nmap [ipaddr] -sv -p21-100
```
で21から100までのポートをスキャン可能(復習)  

ans. vsftpd 3.0.3  

# Task3

ans. 230  

ftpコマンドで対象に対してログインを試みるとユーザネームの入力を求められるので、ここでanonymousを指定。すると230Loging successfulが返ってくるのでこれが答え


# Task4

ans. anonymous  

匿名ユーザとしてftpサーバにログインする場合に用意されている名前  

# Task5

ans. get  

ftpclientとしてダウンロードをするために使用するコマンド

# Task6

lsコマンドでftpサーバに置かれているファイルを確認すると、問題文にあるようにallowed.userlistファイルが存在する事が確認できる。これを`get allowed.userlist`で落として中身を確認したところ、権限の高そうなユーザ名としてadminがあることが確認できた。  

ans. admin

# Task7

`nmap [ipaddr] -sV -p 80`でサービスバージョン検出

ans. Apache httpd 2.4.41

# Task8

`gobuster dir -h`でgobusterのdirコマンドヘルプを開くと、dirの後に-xのフラグを立てることで、指定した拡張子のファイルを検索するよう指定できることが書いてある。  

# Task9

`gobuster dir -u 10.129.158.209 -w /usr/share/wordlists/dirbuster/directory-list-2.3-small.txt -x php`でブルートフォース攻撃が開始される  

dirはディレクトリを探索するということ、-uはurlの指定を行うフラグ、-wは使用するワードリストを指定するフラグ、-xはどの拡張子のファイルを調査対象とするかの指定で,区切りで複数の拡張子を指定可能  
これによって、認証を行っていると思わしきphpファイルlogin.phpが発見できた

ans. login.php

# Task10

ftpで対象のサーバにアクセスし、allowed.userlistとallowed.userlist.passwdを取得しておく。allowed.userlistにはadmingというユーザが4行目に登録されており、passwdのほうでは4行目にパスワードらしき文字列が確認できた。  
Task9でlogin.phpというファイルが存在していることが分かったことから、ipaddr/login.phpにブラウザでアクセスを行う。ログイン情報を入力されるよう促されるので、adminとそれに対応すると思われるパスワードを入力すると、フラグを取得できる。  
