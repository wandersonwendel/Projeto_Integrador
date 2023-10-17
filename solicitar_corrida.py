import pika

def solicitar_corrida(email, endereco, endereco_destino):
    mensagem = f"{email};{endereco};{endereco_destino}"

    # Conectar ao RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
    channel = connection.channel() 

    # Publicar a mensagem na fila de solicitação de corrida
    channel.basic_publish(exchange='', routing_key='fila_solicitar_corrida', body=mensagem)

    print(f"Solicitação enviada: {mensagem}")
    
    connection.close()

# Exemplo de uso
solicitar_corrida('wandersonsousa489@gmail.com', 'Hotel', 'Praia')
solicitar_corrida('wandersonsousa489@gmail.com', 'Praia', 'Hotel')
