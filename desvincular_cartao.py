import pika

def enviar_desvinculacao(email, numero_cartao):
    mensagem = f"{email};{numero_cartao}"

    # Conectar ao RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
    channel = connection.channel() 

    # Publicar a mensagem na fila
    channel.basic_publish(exchange='', routing_key='fila_desvincular_cartao', body=mensagem)

    print(f'Solicitação de desvinculação de cartão enviada: {mensagem}')

    connection.close()

# Para desvincular um cartão
enviar_desvinculacao('joao@email.com', '1234567890123456')