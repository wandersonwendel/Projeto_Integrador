import pika

def solicitar_corrida(email, endereco_partida, endereco_destino):
    mensagem = f"{email};{endereco_partida};{endereco_destino}"

    # Conectar ao RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
    channel = connection.channel() 

    # Publicar a mensagem na fila de solicitação de corrida
    channel.basic_publish(exchange='', routing_key='fila_solicitacao_corrida', body=mensagem)

    valor_da_corrida = 5.0
    print(f"Valor da corrida: R${valor_da_corrida}")

    solicitar_corrida = int(input("Solicitar corida: 1(Sim), 2(Não)"))
    if solicitar_corrida == 1:
        print("Corrida solicitada. Seu motorista irá chegar em breve!")
    elif solicitar_corrida == 2:
        print("Corrida cancelada!")
    
    connection.close()

# Exemplo de uso
solicitar_corrida('usuario@example.com', 'Endereço de Partida', 'Endereço de Destino')
