import pika

def cadastrar_mototaxi(email, disponivel, latitude, longitude):
    mensagem = f"{email};{disponivel};{latitude};{longitude}"

    # Conectar ao RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672)) 
    channel = connection.channel() 

    # Publicar a mensagem na fila
    channel.basic_publish(exchange='', routing_key='fila_cadastrar_mototaxi', body=mensagem)

    print(f'Mensagem enviada: {mensagem}')

    connection.close()

# Exemplo de uso
cadastrar_mototaxi('wandersonsousa489@gmail.com', True , '5', '10')