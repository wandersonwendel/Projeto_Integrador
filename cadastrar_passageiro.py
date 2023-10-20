import pika

def cadastrar_usuario(nome, email, telefone, senha, endereco, sexo):
    mensagem = f"{nome};{email};{telefone};{senha};{endereco};{sexo}"

    # Conectar ao RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
    channel = connection.channel() 

    # Publicar a mensagem na fila
    channel.basic_publish(exchange='', routing_key='fila_cadastrar_passageiro', body=mensagem)

    print(f'Mensagem enviada: {mensagem}')

    connection.close()

# Exemplo de uso
cadastrar_usuario('Wanderson', 'wandersonsousa489@gmail.com', '00972844', 'lllksk', 'ksdhjfuigud', 'senha123')