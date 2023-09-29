import pika
import psycopg2
import bcrypt

def cadastrar_usuario(nome, email, telefone, senha, endereco, sexo):
    # Conectar ao banco de dados PostgreSQL
    try:
        conn = psycopg2.connect(database="itaxi", user="postgres", password="1234", host="localhost", port="5432")
        cursor = conn.cursor()
    except psycopg2.Error as e:
        print(f"Erro ao se conectar com o Banco de Dados: {e}!")

    # Verificar se o usuário já está cadastrado
    cursor.execute("SELECT * FROM usuarios WHERE email=%s", (email,))
    usuario = cursor.fetchone()

    if usuario is None:
        # Inserir novo usuário no banco de dados
        cursor.execute("INSERT INTO usuarios (nome, email, telefone,senha, endereco, sexo) VALUES (%s, %s, %s, %s, %s, %s)",
                       (nome, email, telefone, senha, endereco, sexo))
        conn.commit()

        print(f"Usuário {email} cadastrado com sucesso!")
    else:
        print(f"Usuário com o Email {email} já está cadastrado.")

    cursor.close()
    conn.close()

def callback(ch, method, properties, body):
    mensagem = body.decode('utf-8')
    nome, email, telefone, senha, endereco, sexo= mensagem.split(';')
    senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
    try:
        cadastrar_usuario(nome, email, telefone, senha, endereco, sexo)
    except Exception as e:
        print(f"Erro ao processar mensagem: {e}")

# Conectar ao RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))

channel = connection.channel()

# Definir a fila a ser consumida
channel.queue_declare(queue='fila_cadastro')

# Configurar o callback para receber mensagens
channel.basic_consume(queue='fila_cadastro', on_message_callback=callback, auto_ack=True)

print('Aguardando mensagens...')
channel.start_consuming()