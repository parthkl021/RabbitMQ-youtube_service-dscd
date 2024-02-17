import pika
import json
import threading

subscriptions = {}
# youtube_server = input('Enter IP: ')
def consumer_user_requests():
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_declare(queue='uefa_champions', durable=True)

    def callback(ch, method, properties, body):
        data = json.loads(body.decode())
        user = data['user']
        youtuber = data['youtuber']
        is_subscribed = data['subscription']
        
        if is_subscribed:
            if youtuber not in subscriptions:
                subscriptions[youtuber] = []
            if user not in subscriptions[youtuber]:
                subscriptions[youtuber].append(user)
        else:
            if youtuber in subscriptions and user in subscriptions[youtuber]:
                subscriptions[youtuber].remove(user)
        
        print(f"Updated subscriptions: {subscriptions}")

    channel.basic_consume(queue='uefa_champions', on_message_callback=callback, auto_ack=True)
    print('Listening for user subscription requests...')
    channel.start_consuming()

def notify_user(user, youtuber, videoName):
    connection = pika.BlockingConnection(pika.ConnectionParameters("0.0.0.0"))
    channel = connection.channel()
    queue_name = f"{user}_noti"
    channel.queue_declare(queue=queue_name, durable=True)
    notification = {'youtuber': youtuber, 'videoName': videoName}
    body = json.dumps(notification)
    channel.basic_publish(exchange='', routing_key=queue_name, body=body,
                          properties=pika.BasicProperties(delivery_mode=2))
    print(f"Notification sent to {user}: {body}")
    connection.close()

def consumer_youtuber_requests():
    connection = pika.BlockingConnection(pika.ConnectionParameters("0.0.0.0"))
    channel = connection.channel()
    channel.queue_declare(queue='ytup', durable = True)

    def callback(ch, method, properties, body):
        data = json.loads(body.decode())
        youtuber = data['youtuber']
        videoName = data['videoName']
        
        if youtuber in subscriptions:
            for user in subscriptions[youtuber]:
                notify_user(user, youtuber, videoName)

    channel.basic_consume(queue='ytup', on_message_callback=callback, auto_ack=True)
    print('Listening for new videos from YouTubers...')
    channel.start_consuming()        

if __name__ == '__main__':
    # Create threads for consumer functions
    user_thread = threading.Thread(target=consumer_user_requests)
    youtuber_thread = threading.Thread(target=consumer_youtuber_requests)
    
    # Start threads
    user_thread.start()
    youtuber_thread.start()
    
    # Wait for all threads to complete
    user_thread.join()
    youtuber_thread.join()
