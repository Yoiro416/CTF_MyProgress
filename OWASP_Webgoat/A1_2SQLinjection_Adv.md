# (A1)Injection(Advanced) 節の問題の回答
さらに複雑なSQLinjectionについて学んでいきましょう

## 3 Try It! Pulling data from other tables
まずはuser_system_data table内に存在する全データを取得したいので、UNIONを使用して情報を抜き取りました。Nameのフィールドに次の文を入力しGet Account Infoします。
```SQL
' UNION SELECT userid,user_name,password,cookie,NULL,NULL,NULL FROM user_system_data;--
```
この入力を基に組み立てられる命令は、
```SQL
SELECT * FROM user_data WHERE last_name = '' UNION SELECT userid,user_name,password,cookie,NULL,NULL,NULL FROM user_system_data;--'
```
となるはずです。先頭から順に解説します。  
まずuser_dataからlast_nameが''に該当する人のすべてのcolumnのデータが抽出されます。last_nameにnot nullやprimary keyの制約がないとはいえ何も返さないほうが多いでしょう。  
次に、UNIONでテーブルの情報の和集合を得ます。上記のように、一方のテーブルから得られる情報が無と仮定するなら、単純にUNIONの後ろのSELECT文で取得できるテーブルを見ることができます。  
UNION以降のSELECTで、わざわざuserid,...,NULL,NULL,NULLと抽出するcolumnをNULLで水増ししているのは、UNIONでテーブルの情報をまとめる場合、columnの数を統一する必要があるためです。NULLの部分はテーブルで定義されているデータ型に合わせて'a','b',1でも動きますが、NOT NULL制約がない限りNULLはcolumnのデータ型がvarcharでもintでも有効なためこちらのほうが楽かと思います。  
あとは取得したDaveのパスワードを入力してクリアです。

## 5 Blind SQL injection
直接データを抽出するのではなく、条件式の真偽を用いてデータを取得するBlind SQL injectionについて学びます。
条件式を繰り返し実行して一文字ずつ結果を得ていくので、プログラムによる自動化を用います。sniper.pyを参照してください。  
まずはLOGINの欄を見てみます。F12を使ってログイン処理を追いかけてみるが踏み台になりそうな情報はぱっと見て特になし。おそらくusernameを使ってpasswordを検索し、それが合致するかを確認しているのでは？と思ったが'を入力してもエラーが変わらない。特殊文字に対するエスケープが働いているか認証の仕組みが予想とは違うか...とにかく別の方法を試してから考えてみることにしました。  
次にREGISTERの欄を確認します。同じくネットワークを監視しながらとりあえず登録してみます。username_regやemail_regなどの内容には特殊文字などは入れずとりあえず動作だけ確認。問題なく登録できました。  
ここで、同じ名前で登録しようとすると
```
User [入力した名前] already exists please try to register with a different username.
```
と表示されることを確認しました。そしてREGISTERのusername欄に'を入力すると
```
Something went wrong
```
と帰ってくることが確認できました。おそらくここに脆弱性が存在すると予想し、プログラムを作成していきます。  
Username欄に name' AND 1=2;-- と入力すると、User name' AND 1=2;-- created という応答が返ってきました。これは同じ内容で何度入力しても同じ応答が返ってくるので、userに重複があるかチェックするSQL文が実行されており、そのチェックの結果がFALSEならば重複なしとして処理しているようです。  
つまり、1=2の部分を1=1にすると？変わりました。Already exists...と帰ってきます。
ここで、1=1にした場合に結果が変わるのは既に存在するusernameに対してのみのようです。条件式のANDより左側でFALSE(そもそもユーザが存在しない)と評価されると、右の条件が何であれ全体としてFALSEになってしまうためだと考えられます。 
ここまで情報が集まれば、POSTを利用して通信をしていることはわかっているため、どのようなpayloadが作成されているかを調べながらプログラミングしていきます。以降のプログラムに関する詳細な説明はsniper.py内部のコメントアウトを参照ください。  
取得したパスワードを使い、TomとしてLOGINすればクリアです。

## 6 知識クイズ
私にとっては英語力クイズでもあります。
### 1. What is the difference between a prepared statement and a statement?
1. Prepared statementは事前にコンパイルを行っているため、Statementよりも高速な傾向があります。**Ans.4**
2. プレースホルダ内の変数は?を使って表現します。**Ans.3**
3. 1.にもあったように、事前にコンパイルをしておくことで高速に動作できます。**Ans.2**
4. プレースホルダはSQLのQueryとユーザからの入力を分離することでinjectionを防ぐことができます。**Ans.3**
5. Prepared statementは4.にもあるようにユーザからの入力とSQLのQueryを分離します。つまり、ユーザからの入力は単なる文字列として扱われ、全文が登録されます。**Ans.4**