import pika
import psycopg2

DISTANCIA_MAXIMA = 1  

def conectar_banco(): 
    return psycopg2.connect(database="itaxi", user="postgres", password="1234", host="localhost", port="5432")

def obter_mototaxis_disponiveis(cliente_x, cliente_y):
    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute("SELECT id, latitude, longitude FROM mototaxis")
    mototaxis = cursor.fetchall()

    mototaxis_proximos = []

    for mototaxi in mototaxis:
        mototaxi_id, mototaxi_x, mototaxi_y = mototaxi
        distancia = ((cliente_x - mototaxi_x)**2 + (cliente_y - mototaxi_y)**2)**0.5

        if distancia <= DISTANCIA_MAXIMA:
            mototaxis_proximos.append({'id': mototaxi_id, 'distancia': distancia})

    cursor.close()
    conn.close()

    return mototaxis_proximos

def callback(ch, method, properties, body):
    mensagem = body.decode('utf-8')
    partes = mensagem.split(';')
    
    if partes[0] == "SOLICITACAO":
        cliente_id = int(partes[1])
        mototaxi_id = int(partes[2])

        mototaxi_disponivel = True  # Simulação
        if mototaxi_disponivel:
            print(f"Solicitação de corrida do cliente {cliente_id} para o mototaxi {mototaxi_id}")

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
channel = connection.channel()
channel.queue_declare(queue='fila_solicitacoes_corrida')
channel.basic_consume(queue='fila_solicitacoes_corrida', on_message_callback=callback, auto_ack=True)

print('Aguardando mensagens...')
channel.start_consuming()
