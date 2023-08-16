import pika as pk
A = 2
B = 6
iterations = 0
connection = pk.BlockingConnection(pk.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='multiplication')

def multiply(max_iterations):
    def callback(ch, method, properties, body):
        global A
        X  = A * int(body)
        A = X
        print("After multiplication function: ", X)
        channel.basic_publish(exchange='', routing_key='multiplication', body=str(X))
        global iterations
        print("iteration Number :", iterations)
        iterations += 1
        if iterations == max_iterations:
            connection.close()
            
    channel.basic_consume(queue='square', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

required_iterations=int(input("Enter an integer for max iterations: "))
multiply(required_iterations)
