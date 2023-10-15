import pika

def enviar_mensagem(placa, crlv, fotoCNH, corVeiculo, modeloVeiculo, anoVeiculo, renavam, numeroChassi):
    mensagem = f"{placa};{crlv};{fotoCNH};{corVeiculo};{modeloVeiculo};{anoVeiculo};{renavam};{numeroChassi}"

    # Conectar ao RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
    channel = connection.channel()  

    # Publicar a mensagem na fila
    channel.basic_publish(exchange='', routing_key='fila_cadastro_veiculo', body=mensagem)

    print(f'Mensagem enviada: {mensagem}')

    connection.close()

# Exemplo de uso
enviar_mensagem('abc123', '(Documento)', '(Documento)', 'rosa', 'Peugeot', '2020', '12345678912', '99913493045421')
