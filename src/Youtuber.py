import pika
import sys
import json
import os

youtuber_id = input('Enter IP: ')
def main():
    # Check if at least three arguments are passed (the script name, youtuber name, and at least one word for the video name)
    if len(sys.argv) >= 3:
        youtuber = sys.argv[1]
        # Join all remaining arguments to form the videoName, allowing for multi-word titles
        videoName = " ".join(sys.argv[2:])
        
        print(f'youtuber: {youtuber}')
        print(f'videoName: {videoName}')
        
        # Establish a connection to RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters(youtuber_id))
        channel = connection.channel()
        
        # Declare a queue named after the YouTuber
        channel.queue_declare(queue='ytup', durable=True)
        
        # Prepare and publish the message
        body = json.dumps({'youtuber': youtuber, 'videoName': videoName})
        channel.basic_publish(exchange='', routing_key='ytup', body=body, 
                              properties=pika.BasicProperties(delivery_mode=2))
        print(f" [x] Sent {body}")
        print("SUCCESS")
    else:
        print('Invalid Input')
        sys.exit(0)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
