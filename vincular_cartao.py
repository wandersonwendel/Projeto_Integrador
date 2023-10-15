import pika

def enviar_vinculacao(email, numero_cartao, nome_titular, data_validade, codigo_seguranca):
    mensagem = f"{email};{numero_cartao};{nome_titular};{data_validade};{codigo_seguranca}"

    # Conectar ao RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.3.6', port=5672))
    channel = connection.channel()

    # Publicar a mensagem na fila
    channel.basic_publish(exchange='', routing_key='fila_vincular_cartao', body=mensagem)

    print(f'Solicitação de vinculação de cartão enviada: {mensagem}')

    connection.close()

# Exemplos de uso
enviar_vinculacao('joao@email.com', '1234567890123456', 'João Silva', '12/23', '123')
