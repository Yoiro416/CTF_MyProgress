# Starting point Tier2 : Sequel

## Task1

```shell
nmap [ipaddr]
```

の結果、3006/tcpで発見

## Task2

```shell
sudo nmap -sV -sC [ipaddr]
```

このコマンドは、対象に向けて`-sV`でターゲット上で稼働しているソフトのバージョンを検出すること、`-sC`でデフォルトスクリプトを有効化している。  
スクリプトは、通常TCP/UDPの要求を投げているのに上乗せしてスクリプトを実行している。セキュリティ的に侵入的であるとみなされるので絶対に公共のネットワークで(許可なく)打たないこと。とはいえ今回はこれで詳細が取得できた。  

```txt
┌──(kali㉿kali)-[~]
└─$ sudo nmap -sV -sC 10.129.128.165
Starting Nmap 7.93 ( https://nmap.org ) at 2023-12-21 22:26 EST
Nmap scan report for 10.129.128.165
Host is up (0.20s latency).
Not shown: 999 closed tcp ports (reset)
PORT     STATE SERVICE VERSION
3306/tcp open  mysql?
| mysql-info: 
|   Protocol: 10
|   Version: 5.5.5-10.3.27-MariaDB-0+deb10u1
|   Thread ID: 135
|   Capabilities flags: 63486
|   Some Capabilities: Support41Auth, Speaks41ProtocolOld, IgnoreSigpipes, FoundRows, DontAllowDatabaseTableColumn, IgnoreSpaceBeforeParenthesis, ConnectWithDatabase, SupportsTransactions, ODBCClient, InteractiveClient, Speaks41ProtocolNew, SupportsLoadDataLocal, LongColumnFlag, SupportsCompression, SupportsMultipleResults, SupportsAuthPlugins, SupportsMultipleStatments
|   Status: Autocommit
|   Salt: vpNu%TV6HGmmZ]E!r=wb
|_  Auth Plugin Name: mysql_native_password
```

動いているのはMariaDB

## Task3

`-u`オプションでユーザを指定してログインする

## Task4

rootユーザを使用すればパスワード無しでログイン可能

## Task5

要するにwildecard  
お馴染み`*`が正解  

## Task6

Cと同じく`;`が必要。  
インタプリタなら忘れても追加で打てばいいだけだがスクリプトなどに起こすなら忘れなように  

## Task7

```SQL
SHOW DATABASES;
```

でDBの様子を把握する。するとデフォルトのDB以外に`htb`が発見できた。  

## Task8

```SQL
USE htb
SHOW TABLES;
SELECT * FROM users;
SELECT * FROM config;
```

configテーブルからの抽出でflagを発見できた。
