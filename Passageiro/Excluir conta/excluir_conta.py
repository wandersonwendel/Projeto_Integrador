import pika

def excluir_conta(nome, email, telefone, senha, endereco, sexo):
    mensagem = f"{nome};{email};{telefone};{senha};{endereco};{sexo}"

    # Conectar ao RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672)) 
    channel = connection.channel() 

    # Publicar a mensagem na fila
    channel.basic_publish(exchange='', routing_key='fila_excluir_conta', body=mensagem)

    print(f'Mensagem enviada: {mensagem}')

    connection.close()

# Exemplo de uso
excluir_conta('Wanderson', 'wandersonsousa489@gmail.com', '00972844', 'lllksk', 'ksdhjfuigud', 'senha123')