import pika

def login_passageiro(email, senha):
    mensagem = f"{email};{senha}"

    # Conectar ao RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672)) 
    channel = connection.channel() 

    # Publicar a mensagem na fila
    channel.basic_publish(exchange='', routing_key='fila_login_passageiro', body=mensagem)

    print(f'Mensagem enviada: {mensagem}')

    connection.close()

# Exemplo de uso
login_passageiro('wandersonsousa489@gmail.com', 'lllksk')