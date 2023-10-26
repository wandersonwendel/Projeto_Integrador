import pika

def vincular_cartao(email, numero_cartao, nome_titular, data_validade, cvv):
    mensagem = f"{email};{numero_cartao};{nome_titular};{data_validade};{cvv}"

    # Conectar ao RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
    channel = connection.channel()

    # Publicar a mensagem na fila 
    channel.basic_publish(exchange='', routing_key='fila_vincular_cartao', body=mensagem)

    print(f'Solicitação de vinculação de cartão enviada: {mensagem}')

    connection.close()

# Exemplos de uso
vincular_cartao('wandersonsousa489@gmail.com', '1234567890123456', 'Wanderson', '12/23', '123')
