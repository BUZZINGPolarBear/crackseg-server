import json

import pika

# RabbitMQ에 연결
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# 수신할 큐 이름
queue_name = 'Q_API'

# 큐 삭제
channel.queue_delete(queue='Q_API')

# 큐 선언
channel.queue_declare(queue='Q_API', durable=True)

def runInference(ch, method, properties, body):
    print("------- 이미지 균열 조사 시작 --------")
    # byte를 문자열로 디코딩
    string_message = body.decode('utf-8')
    json_message = json.loads(string_message)

    origId = json_message['analysisId']
    index = json_message['index']
    fileDir = json_message['fileDir']
    distance = json_message['distance']
    print(f"body: {origId} {index} {fileDir} {distance}")


# 큐에 콜백 함수를 등록하여 메시지 수신 대기
channel.basic_consume(queue=queue_name, on_message_callback=runInference, auto_ack=True)

# 메시지 수신 시작
channel.start_consuming()