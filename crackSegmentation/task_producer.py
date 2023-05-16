import pika
import json
# RabbitMQ에 연결
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# 송신할 큐 이름
queue_name = 'Q_API'

# 큐에 메시지 송신
# 헤더와 바디 데이터 생성
header = {
    "op": "image_analysis",
    "type": "req",
    "tid": "1682993290557",
    "msgFrom": "Q_API",
    "timestamp": "2023-05-02 11:08:10.557"
}

body = {
    "origId": "e32d2e35EZ33846Azx33",
    "analysisId": "d277323f23aa425abd4cd772ceba5566",
    "index": 3,
    "fileDir": "/Users/joonhwi/Desktop/KAU/5-1/capstone/crack_semantic_segmentation/crack_segmentation_dataset/images/CFD_001.jpg",
    "distance": "4.71"
}

# 메시지 생성
message = {
    "header": header,
    "body": body
}
# 메시지를 JSON 형식으로 직렬화
message_json = json.dumps(message['body'])

# 큐에 메시지 송신
channel.basic_publish(exchange='', routing_key=queue_name, body=message_json)

# 연결 종료
connection.close()