# Youtube service using RabbitMQ

## Dependencies
1. pika: `pip install pika`

## How to run
1. Install RabbitMQ server on the server-side   
    `sudo apt install rabbitmq-server`

2. Create config file to allow guest users to connect remotely   
    `sudo nano /etc/rabbitmq/rabbitmq.conf`
    
    Add following line to it   
    `loopback_users = none`

3. Start the rabbitmq-server   
    `sudo systemctl start rabbitmq-server`   
    `sudo systemctl enable rabbitmq-server`

4. Start the YoutubeServer   
    `python YoutubeServer.py`

5. Create a Youtuber and upload video   
    `python Youtuber.py [name] [video_name]`

6. Create a user and subscribe to a youtuber   
    Subscribe: `python User.py [username] [youtuber_name] s`   
    Unsubscribe: `python User.py [username] [youtuber_name] u`   
    Login: `python User.py [username]`

### Misc
https://www.cherryservers.com/blog/how-to-install-and-start-using-rabbitmq-on-ubuntu-22-04

