import pika as pk

A = 2
B = 6
iterations=0

connection = pk.BlockingConnection(pk.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='square')

def square(required_iterations):
    channel.basic_publish(exchange='', routing_key='square', body=str(B))
    def callback(ch, method, properties, body):
        X = int(body)** 2
        print("After square : ", X)
        channel.basic_publish(exchange='', routing_key='square', body=str(X))
        global iterations
        iterations+=1
        if iterations==required_iterations:
           connection.close()
        print("Iteration Number :", iterations)
        
    channel.basic_consume(queue='multiplication', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
required_iterations=int(input("Enter an integer for max iterations: "))
square(required_iterations)
