import pika
import sys
import json
import os

user_id = input('Enter IP: ')
list_of_users = []
def main():
    if len(sys.argv) == 2:
        username = sys.argv[1]
        print(f'username: {username}')
        uefa_champions = 'uefa_champions'
        # Establish connection to RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters(user_id))
        channel = connection.channel()
        # Declare a queue for the user
        channel.queue_declare(queue=uefa_champions, durable=True)
        # Prepare the body for login (no youtuber or subscription action)
        body = json.dumps({'user': username, 'youtuber': '', 'subscription': False})
        channel.basic_publish(exchange='', routing_key=uefa_champions, body=body,
                              properties=pika.BasicProperties(delivery_mode=2))
        print(f" [x] Sent {body}")
        list_of_users.append(username)
        
    elif len(sys.argv) == 4:
        username = sys.argv[1]
        youtuber = sys.argv[2]
        subscription_action = sys.argv[3]
        uefa_champions = 'uefa_champions'
        print(f'username: {username}')

        subscribe = True if subscription_action == 's' else False

        connection = pika.BlockingConnection(pika.ConnectionParameters(user_id))
        channel = connection.channel()
        # Declare a queue for the user
        channel.queue_declare(queue=uefa_champions, durable=True)
        # Prepare the body with user, youtuber, and subscription action
        body = json.dumps({'user': username, 'youtuber': youtuber, 'subscription': subscribe})
        channel.basic_publish(exchange='', routing_key=uefa_champions, body=body,
                              properties=pika.BasicProperties(delivery_mode=2))
        print(f" [x] Sent {body}")
        list_of_users.append(username)

    else:
        print('Invalid Input')
        sys.exit(0)
    
    connection = pika.BlockingConnection(pika.ConnectionParameters(user_id))
    channel = connection.channel()

    for username in list_of_users:
        notification_queue = f"{username}_noti"
        channel.queue_declare(queue=notification_queue, durable=True)

        def callback(ch, method, properties, body):
            notification = json.loads(body.decode())
            print(f"Notification for {username}: {notification}")

        channel.basic_consume(queue=notification_queue, on_message_callback=callback)
        print(f'Listening on {notification_queue} for messages. To exit press CTRL+C')
    
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print('Interrupted')
        connection.close()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
