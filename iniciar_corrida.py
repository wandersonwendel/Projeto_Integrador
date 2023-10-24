import pika

def iniciar_corrida(email, mototaxi, corrida_aceita, localizacao_atual, origem, destino):
    mensagem = f"{email};{mototaxi};{corrida_aceita};{localizacao_atual};{origem};{destino}"

    # Conectar ao RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
    channel = connection.channel() 

    # Publicar a mensagem na fila
    channel.basic_publish(exchange='', routing_key='fila_iniciar_corrida', body=mensagem)

    print(f'Mensagem enviada: {mensagem}')

    connection.close()


# Chamar a função iniciar_corrida com os parâmetros adequados
iniciar_corrida('wandersonsousa489@gmail.com', 'Roger', True, 'Hotel', 'Hotel', 'Praia')