# импортируем flack и запускаем Web сервер
from flask import Flask, abort, request
import json
import datetime
from pprint import pprint
import requests
import shutil

# определяем начальные значения переменных

t1 = datetime.datetime.now()
pprint ("Скрипт запущен в " + str(t1))

server = Flask(__name__)
# декоратор
@server.route('/codec', methods=['POST'])

def codec():
    global t1

    if not request.json:
        abort(400)
    parsed_request = request.json

# ловим feedback и опрделяем сколько людей в комнате

    people = parsed_request['Status']['RoomAnalytics']['PeopleCount']['Current']['Value']
    pprint ("Число людей в комнате:"+people)

    if int(people) >= 0:
#        pprint ("Их больше или равно 0 (не отрицательное значение")
        pprint("было " + str(t1) + ", стало " + str(datetime.datetime.now()))
        realdelta = (datetime.datetime.now() - t1)
        t1 = datetime.datetime.now()

        if realdelta > datetime.timedelta(seconds=10):
            pprint ("Задержка в " + str(realdelta.seconds) + "секунд выдержана")
            getlocalview('spark room kit'+t1.strftime("%Y-%m-%d_%H.%M.%S")+'.jpeg','10.100.1.103', 'admin', 'C1sco123')
#            save2file(t1.strftime("%Y-%m-%d %H.%M.%S")  + ' , ' + people + '\n')
            save2file(t1.strftime("%H.%M") + ',' + people + '\n')
        else:
            pprint("прошло не достаточно времени - " + str(realdelta.seconds) + "секунд")

    return 'ok'

def register_webhook():
    import requests

    url = "http://10.100.1.103/putxml"

    payload = "<Command>\r\n   <HttpFeedback>\r\n      <Register>\r\n         <FeedbackSlot>1</FeedbackSlot>\r\n         <ServerUrl>http://10.100.1.138:5000/codec</ServerUrl>\r\n         <Format>JSON</Format>\r\n         <Expression item=\"1\">/Status/RoomAnalytics/PeopleCount</Expression>\r\n        </Register>\r\n   </HttpFeedback>\r\n</Command>"
    headers = {
        'content-type': "text/xml",
        'authorization': "Basic YWRtaW46QzFzY28xMjM=",
        'cache-control': "no-cache",
        'postman-token': "2fd8d890-5a65-50ce-1392-cb213faeb47c"
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)

def getlocalview(name, ip, user, password):

#    url = "http://"+ip+"/websnapshot/get"
    response = requests.get('http://'+ip+'/websnapshot/get', stream=True, verify=False, auth=(user, password))
    with open(name, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response

def save2file(record):
    file=open("people.csv","a")
    file.write(record)
    file.close()

register_webhook()
if __name__ == '__main__':

    server.run(host='0.0.0.0', port=5000, debug=True)



