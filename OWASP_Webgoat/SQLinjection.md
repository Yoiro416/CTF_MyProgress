# (A1)Injection 節の問題の回答
## 2 What is SQL?の回答
まずはSQLの基本の確認から。ここではAdmin権限をすでに得ているため普通のQueryを組み立てます
```SQL
SELECT department FROM employees WHERE first_name = 'Bob' and last_name = 'Franco';
```
Tableの内容も見えているので、Bob Franco氏のdepartmentを抽出してクリア。
このテーブルの内容ならand last name = 'Franco'はなしでも動くとは思いますが一応記述します。

## 3 Data Manipulation Language の回答
上と同じくAdmin権限は持っているので、言われた通りTableの内容を書き換えます
```SQL
UPDATE employees SET department = 'Sales' WHERE first_name = 'Tobi' AND last_name = 'Barnett';
```
