# Titanic (Easy)

date: 2025-02-17

## User Flag

```sh
nmap $TARGET -sV -sC            
Starting Nmap 7.93 ( https://nmap.org ) at 2025-02-17 14:06 JST
Nmap scan report for 10.10.11.55
Host is up (0.18s latency).
Not shown: 987 closed tcp ports (conn-refused)
PORT      STATE    SERVICE        VERSION
22/tcp    open     ssh            OpenSSH 8.9p1 Ubuntu 3ubuntu0.10 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 73039c76eb04f1fec9e980449c7f1346 (ECDSA)
|_  256 d5bd1d5e9a861ceb88634d5f884b7e04 (ED25519)
80/tcp    open     http           Apache httpd 2.4.52
|_http-title: Did not follow redirect to http://titanic.htb/
|_http-server-header: Apache/2.4.52 (Ubuntu)
1198/tcp  filtered cajo-discovery
1658/tcp  filtered sixnetudr
3005/tcp  filtered deslogin
3986/tcp  filtered mapper-ws_ethd
5002/tcp  filtered rfe
5051/tcp  filtered ida-agent
8500/tcp  filtered fmtp
9415/tcp  filtered unknown
27000/tcp filtered flexlm0
27353/tcp filtered unknown
50800/tcp filtered unknown
Service Info: Host: titanic.htb; OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 36.65 seconds
```

とりあえず、httpでのアクセスが`titanic.htb`にリダイレクトされるものの到達できないため、`/etc/hosts`ファイルに

```txt
[target_ip] titanic.htb
```

のエントリを追加してアクセスできるようにする。  

サイトでは旅行計画の登録ができた。POSTにて送信される。Full Name,Email address,Phone Number, Travel date, Cabin Typeを入力してPOSTで送信する。  

ペイロードは次の通り。なお、cabinはStandard,Delux,Suiteの選択方式。  

```md
name=foo&email=bar%40mail.com&phone=000000000&date=3333-11-22&cabin=Standard
```

とりあえずresend機能で内容を書き換えながら試してみた感じ、nameに特殊文字を入れたとき、cabinに未定義の値を設定したときにmethod not allowedで拒否される。emailの値で@(%40)が存在しないデータを無理やり送信すると返答が返ってこない。  

送信が正常に行われると、JSONが返ってくる。例えば次のように、入力した内容が記録される。

```json
{
    "name": "foo",
    "email": "foo@mail.com",
    "phone": "000000000",
    "date": "2025-05-01",
    "cabin": "Standard"
}
```

`ffuf -u http://titanic.htb/FUZZ -w /usr/share/seclists/Discovery/Web-Content/raft-medium-words.txt -fc 301`でサブディレクトリ列挙を行った際に、次のサブディレクトリが発見された。  

- `book`
- `server-status`

ただし、`server-status`に単純にアクセスを試みてもHTTP response code 403 で拒否される。  

HTTP Proxyを用いてbookに対するリクエストのbodyとして

```http
name=test; cat /etc/passwd
```

とすると、応答が返ってこない。(他の入力:`<script>alert(1)</script>`などではBad Requestで拒否される)

もう少し別の方法を探ってみる

`gobuster`を用いてサブドメインを列挙してみる

`gobuster vhost -u http://titanic.htb -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-5000.txt --append-domain -r`でseclistsを使って探索を行う。また、リダイレクトによってstatus code301で`titanic.htb`に飛ばされるので`-r`で対処した

ここで`dev.titanic.htb`というサブドメインが発見できた。`/etc/hosts`に同じIPをセットしてアクセスできるようにすると、Giteaのサービスが動いていることが確認できた。  

Giteaから`flask-app`リポジトリを覗いてみると`app.py`がある。覗いてみるとなんか`/download`がなんか脆弱性がありそう
