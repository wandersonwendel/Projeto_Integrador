import pika
import psycopg2

def conectar_banco():
    return psycopg2.connect(database="itaxi", user="postgres", password="1234", host="localhost", port="5432")

def obter_mototaxis_disponiveis(cliente_x, cliente_y):
    conn = conectar_banco()
    cursor = conn.cursor()

    # Verificando os mototaxis disponíveis
    cursor.execute("SELECT id, latitude, longitude FROM mototaxis WHERE disponivel = true")
    mototaxis = cursor.fetchall()

    # Lista
    mototaxis_proximos = []

    for mototaxi in mototaxis:
        mototaxi_id, mototaxi_x, mototaxi_y = mototaxi
        #  Pitagoras para saber a distância do cliente e do mototaxi
        distancia = ((cliente_x - mototaxi_x)**2 + (cliente_y - mototaxi_y)**2)**0.5 

        # Adicionando na lista
        mototaxis_proximos.append({'id': mototaxi_id, 'distancia': distancia})

    cursor.close()
    conn.close()

    return mototaxis_proximos

def enviar_solicitacao(cliente_id, mototaxi_id):
    mensagem = f"SOLICITACAO;{cliente_id};{mototaxi_id}"

    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
        channel = connection.channel()

        channel.basic_publish(exchange='', routing_key='fila_solicitacao_corrida', body=mensagem)

        print(f'Solicitação de corrida: {mensagem}')

        connection.close()

    except Exception as e:
        print(f"Ocorreu um erro ao conectar-se ao RabbitMQ: {e}")

def callback(ch, method, properties, body):
    mensagem = body.decode('utf-8')
    partes = mensagem.split(';')
    
    if partes[0] == "RESPOSTA": # Processo do pedido de corrida
        status = partes[1]
        
        if status == "ACEITO":
            print("Seu mototaxi está a caminho!")
        elif status == "RECUSADO":
            print("Desculpe, o mototaxi não pode aceitar a solicitação.")
        else:
            print("Resposta desconhecida do entregador.")
    else:
        print("Mensagem desconhecida recebida")

def aguardar_resposta_do_mototaxi(cliente_id):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
    channel = connection.channel()

    # Crie uma nova fila para esta instância do cliente
    queue_name = f'fila_respostas_{cliente_id}'
    channel.queue_declare(queue=queue_name)

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    print('Aguardando o mototaxi aceitar a corrida...')
    channel.start_consuming()

# Autenticação do cliente
email = str(input("Digite o seu Email: ")) # wandersonsousa489@gmail.com

conn = conectar_banco()
cursor = conn.cursor()
cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email,)) # Buscando usuario no banco
cliente = cursor.fetchone()
cursor.close()
conn.close()

if cliente:
    cliente_id = cliente[0]
    print(f"Cliente autenticado! ID: {cliente_id}") # Verificou que aquele e-mail está no banco

    cliente_x = 10  # Exemplo de coordenada x do cliente
    cliente_y = 5   # Exemplo de coordenada y do cliente

    mototaxis_proximos = obter_mototaxis_disponiveis(cliente_x, cliente_y)

    print("Mototaxis próximos:")
    for mototaxi in mototaxis_proximos:
        print(f'ID: {mototaxi["id"]} - Distância: {mototaxi["distancia"]}') 

    mototaxi_escolhido = 1

    enviar_solicitacao(cliente_id, mototaxi_escolhido)

    # Aguardar resposta do entregador
    aguardar_resposta_do_mototaxi(cliente_id)
else:
    print("Email incorreto. Autenticação falhou.")