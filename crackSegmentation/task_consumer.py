import json

import pika
import requests

# RabbitMQ에 연결
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# 수신할 큐 이름
queue_name = 'Q_API'

# 큐 삭제
channel.queue_delete(queue='Q_API')

# 큐 선언
channel.queue_declare(queue='Q_API', durable=True)

# Prefetch Count 설정
channel.basic_qos(prefetch_count=2)

def get_queue_message_count(queue_name):
    url = f"http://localhost:15672/api/queues/%2F/{queue_name}"
    response = requests.get(url, auth=("guest", "guest")) # Replace with your username and password
    data = response.json()

    return data["messages"]

def runInference(ch, method, properties, body):
    print("------- 이미지 균열 조사 시작 --------")
    #byte를 문자열로 디코딩
    string_message = body.decode('utf-8')
    json_message = json.loads(string_message)

    origId = json_message['analysisId']
    index = json_message['index']
    fileDir = json_message['fileDir']
    distance = json_message['distance']
    print(f"body: {origId} {index} {fileDir} {distance}")

    inferenceResult = requests.get(f"http://localhost:8000/crack-seg/run/detailed/mq?fileDir={fileDir}&origId={origId}")
    analyzeCrackResult = requests.get(f"http://localhost:8000/crack-seg/vision-inference?fileDir={fileDir}&origId={origId}")
    print(analyzeCrackResult.text)


# 큐에 콜백 함수를 등록하여 메시지 수신 대기
channel.basic_consume(queue=queue_name, on_message_callback=runInference, auto_ack=False)
# 한 번에 하나의 메시지만 처리하기 위해 prefetch_count 설정
channel.basic_qos(prefetch_count=1)
# 메시지 수신을 위한 루프 실행
try:
    channel.start_consuming()
    print(get_queue_message_count("Q_API"))
except KeyboardInterrupt:
    # 키보드 인터럽트(Ctrl+C)가 발생하면 종료합니다.
    channel.stop_consuming()

# 연결 종료
connection.close()