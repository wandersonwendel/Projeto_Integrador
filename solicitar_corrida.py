import pika

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

def solicitar_corrida(origem, destino, passageiro):
    mensagem = f"{origem};{destino};{passageiro}"

    # Conectar ao RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
    channel = connection.channel()

    # Publicar a mensagem na fila de solicitações de corrida
    channel.basic_publish(exchange='', routing_key='fila_solicitacoes_corrida', body=mensagem)

    print(f'Solicitação de corrida enviada: {mensagem}')

    connection.close()

# Exemplo de uso
solicitar_corrida('Origem A', 'Destino B', 'João')
