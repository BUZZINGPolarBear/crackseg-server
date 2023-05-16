import pika

# RabbitMQ에 연결
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# 송신할 큐 이름
queue_name = 'Q_API'

# 큐에 메시지 송신
message = 'Hello, RabbitMQ!'
channel.basic_publish(exchange='', routing_key=queue_name, body=message)

# 연결 종료
connection.close()