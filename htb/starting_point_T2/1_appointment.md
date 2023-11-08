# Starting point Tier2 : Appointment

## Task1

Acronym "SQL" stand for "Structured Query Language"  

## Task2

SQL Injection

## Task3

Let's googling.  
"A03:2021-Injection"  

## Task4

`nmap [ip_addr] -T5`でざっくりとスキャン。問題でも提示されているがport80が空いているので詳細にここをスキャン  
`nmap [ip_addr] -p 80 -sV`  
これでApache httpd 2.4.38 ((Debian))と動作しているhttp daemonがわかる

## Task5

httpsはWell-known portの443を使用する(標準的に)

## Task6

Directory  
Directory Traversal Attackとかあるよね

## Task7

404 Not Found  
いつものよく見るやつ  

## Task8

Gobusterとかについての参考: [Tools_forHTB](https://note.homie.co.jp/n/n35a6bba8a8a5)  
Ans:dir  
dirオプションでサブドメインを無視してディレクトリを探索できる  

## Task9

MySQLのコメントアウトは、"#","--"がラインでコメントアウト  
"/* comment here */"で複数行コメントアウトができる　　

## Task10

ブラウザを使用して目標IPアドレスの80番ポートへアクセスする。  
ユーザ名欄にadmin'#と入力しadminとしてログインする(ユーザ名の認証は避けられないのでこれ以外だと未知のユーザ名を試すしかなさそう)  
Congratulationsというリターンがある

## Task11

表示されたフラグを入力。ランダム
