import pika

def enviar_mensagem(nome, email, telefone, senha, endereco, sexo):
    mensagem = f"{nome};{email};{telefone};{senha};{endereco};{sexo}"

    # Conectar ao RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
    channel = connection.channel()

    # Publicar a mensagem na fila
    channel.basic_publish(exchange='', routing_key='fila_cadastro', body=mensagem)

    print(f'Mensagem enviada: {mensagem}')

    connection.close()

# Exemplo de uso
enviar_mensagem('Wanderson', 'waandd@gmail.com', '00972844', 'lllksk', 'ksdhjfuigud', 'senha123')