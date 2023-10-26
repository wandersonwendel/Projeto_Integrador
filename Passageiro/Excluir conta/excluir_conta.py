import pika

def excluir_conta(email, senha):
    mensagem = f"{email};{senha}"

    # Conectar ao RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672)) 
    channel = connection.channel() 

    # Publicar a mensagem na fila
    channel.basic_publish(exchange='', routing_key='fila_excluir_conta', body=mensagem)

    print(f'Mensagem enviada: {mensagem}')

    connection.close()

# Exemplo de uso
excluir_conta('wandersonsousa489@gmail.com', 'lllksk')