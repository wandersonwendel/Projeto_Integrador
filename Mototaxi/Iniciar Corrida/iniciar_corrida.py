import pika
import psycopg2

def conectar_banco():
    return psycopg2.connect(database="itaxi", user="postgres", password="1234", host="localhost", port="5432")

def callback_solicitacao_corrida(ch, method, properties, body):
    mensagem = body.decode('utf-8')
    partes = mensagem.split(';')
    
    if partes[0] == "SOLICITACAO":
        cliente_id = int(partes[1])
        mototaxi_id = int(partes[2])

        # Verificar se o mototaxi está disponível
        mototaxi_disponivel = True  # Simulando que esteja
        if mototaxi_disponivel:
            # Simulação: Perguntar se o entregador aceita a solicitação
            resposta = input("Você aceita a solicitação da corrida? (s/n): ")
            if resposta.lower() == 's':
                enviar_resposta_para_cliente(cliente_id, "ACEITO")
            else:
                enviar_resposta_para_cliente(cliente_id, "RECUSADO")
        else:
            print("Não há mototaxis disponíveis no momento.")

def enviar_resposta_para_cliente(cliente_id, status):
    mensagem = f"RESPOSTA;{status};{cliente_id}"

    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
        channel = connection.channel()

        channel.basic_publish(exchange='', routing_key=f'fila_respostas_{cliente_id}', body=mensagem)

        print(f'Resposta de corrida enviada: {mensagem}')

        connection.close()

    except Exception as e:
        print(f"Ocorreu um erro ao conectar-se ao RabbitMQ: {e}")

def aguardar_solicitacao():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
    channel = connection.channel()
    
    channel.queue_declare(queue='fila_solicitacao_corrida')
    channel.queue_declare(queue='fila_encerrar_corrida')
    channel.basic_consume(queue='fila_solicitacao_corrida', on_message_callback=callback_solicitacao_corrida, auto_ack=True)
    channel.basic_consume(queue='fila_encerrar_corrida', on_message_callback=callback_solicitacao_corrida, auto_ack=True)

    print('Aguardando solicitações...')
    channel.start_consuming()

# Exemplo de uso
aguardar_solicitacao()
