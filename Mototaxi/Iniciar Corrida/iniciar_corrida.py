import pika
import psycopg2

def conectar_banco():
    return psycopg2.connect(database="itadelivery", user="postgres", password="1234", host="localhost", port="5432")

def callback(ch, method, properties, body):
    mensagem = body.decode('utf-8')
    partes = mensagem.split(';')
    
    if partes[0] == "SOLICITACAO":
        cliente_id = int(partes[1])
        entregador_id = int(partes[2])

        # Simulação: Verificar se o entregador está disponível
        entregador_disponivel = True  # Simulação
        if entregador_disponivel:
            # Simulação: Perguntar se o entregador aceita a solicitação
            resposta = input("Você aceita a solicitação de entrega? (s/n): ")
            if resposta.lower() == 's':
                enviar_resposta_para_cliente(cliente_id, "ACEITO")
            else:
                enviar_resposta_para_cliente(cliente_id, "RECUSADO")
        else:
            print("Não há entregadores disponíveis no momento.")

def enviar_resposta_para_cliente(cliente_id, status):
    mensagem = f"RESPOSTA;{status};{cliente_id}"

    try:
        credentials = pika.PlainCredentials('admin', '1234')
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
        channel = connection.channel()

        channel.basic_publish(exchange='', routing_key=f'fila_respostas_{cliente_id}', body=mensagem)

        print(f'Resposta de entrega enviada: {mensagem}')

        connection.close()

    except Exception as e:
        print(f"Ocorreu um erro ao conectar-se ao RabbitMQ: {e}")

def aguardar_solicitacao():
    credentials = pika.PlainCredentials('admin', '1234')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue='fila_pedidos')
    channel.basic_consume(queue='fila_pedidos', on_message_callback=callback, auto_ack=True)

    print('Aguardando solicitações...')
    channel.start_consuming()

# Exemplo de uso
aguardar_solicitacao()
