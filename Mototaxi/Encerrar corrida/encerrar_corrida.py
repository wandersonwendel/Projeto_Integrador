import pika
import psycopg2

def conectar_banco():
    return psycopg2.connect(database="itaxi", user="postgres", password="1234", host="localhost", port="5432")

def encerrar_corrida(cliente_id, mototaxi_id):
    mensagem = f"SOLICITACAO;{cliente_id};{mototaxi_id}"

    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
        channel = connection.channel()

        channel.basic_publish(exchange='', routing_key='fila_encerrar_corrida', body=mensagem)

        print(f'Encerrar corrida: {mensagem}')

        connection.close()

    except Exception as e:
        print(f"Ocorreu um erro ao conectar-se ao RabbitMQ: {e}")

def callback_encerrar_corrida(ch, method, properties, body):
    mensagem = body.decode('utf-8')
    partes = mensagem.split(';')
    
    if partes[0] == "RESPOSTA":
        status = partes[1]
        
        if status == "ACEITO":
            print("Corrida encerrada!")
        else:
            print("Resposta desconhecida do mototaxi.")
    else:
        print("Mensagem desconhecida recebida")

def aguardar_resposta_do_mototaxi(cliente_id):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
    channel = connection.channel()

    # Crie uma nova fila para esta instância do cliente
    queue_name = f'fila_respostas_{cliente_id}'
    channel.queue_declare(queue=queue_name)

    channel.basic_consume(queue=queue_name, on_message_callback=callback_encerrar_corrida, auto_ack=True)

    print('Aguardando o mototaxi encerrar a corrida...')
    channel.start_consuming()