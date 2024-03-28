This work is part of our DSCD courework. There are 3 contributors for this work Sachin, Rishav and Me
# Youtube service using RabbitMQ
A simplified version of a YouTube application using RabbitMQ
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

![image](https://github.com/SachinSharma-IIITD/RabbitMQ-youtube_service-dscd/assets/92939004/7dcb5c26-b05e-4f55-badc-8f7caef26555)

