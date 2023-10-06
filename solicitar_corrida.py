import pika

def enviar_mensagem(usuario, origem, destino):
    # Enviar a solicitação de corrida para a fila
    message = f'{usuario};{origem};{destino}'

    # Conectar ao RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
    channel = connection.channel()

    # Publicar a mensagem na fila de corrida
    channel.basic_publish(exchange='', routing_key='fila_solicitar_corrida', body=message)
    print(f'Mensagem enviada: {message}')

    connection.close()  


def enviar_mensagem_iniciar_corrida(motorista):
    channel.basic_publish(exchange='', routing_key='iniciar_corrida', body=message)
    message = f'Motorista {motorista} aceitou a corrida'

    # Conectar ao RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
    channel = connection.channel()

    print(f'Mensagem enviada: {message}')

    connection.close()
    # Simular um motorista aceitando a corrida
    

enviar_mensagem('João', 'Aeroporto', 'Hotel')
enviar_mensagem('Maria', 'Estação de trem', 'Restaurante')
# enviar_mensagem_iniciar_corrida('Motorista1')