import pika
import psycopg2
import bcrypt

def cadastrar_usuario(nome, email, telefone, senha, endereco, sexo):
    # Conectar ao banco de dados PostgreSQ
    try:
        if not nome.strip() or not email.strip() or not telefone.strip() or not senha.strip():
            raise ValueError("Campos obrigatórios em falta")
        
        # Resto do código de cadastro aqui
        conn = psycopg2.connect(database="itaxi", user="postgres", password="1234", host="localhost", port="5432")
        cursor = conn.cursor()

         # Verificar se o usuário já está cadastrado
        cursor.execute("SELECT * FROM usuarios WHERE email=%s", (email,))
        usuario = cursor.fetchone()

        if usuario is None:
            # Inserir novo usuário no banco de dados
            cursor.execute("INSERT INTO usuarios (nome, email, telefone, senha, endereco, sexo) VALUES (%s, %s, %s, %s, %s, %s)",
                           (nome, email, telefone, senha, endereco, sexo))
            conn.commit()
            
            print(f"Usuário {email} cadastrado com sucesso!")
        else:
            print(f"Usuário com o email {email} já está cadastrado!")

        cursor.close()
        conn.close()

    except ValueError as e:
        print(f"Erro ao cadastrar usuário: {e}")

    except psycopg2.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")

    except Exception as e:
        print(f"Erro inesperado ao cadastrar usuário: {e}")

def cadastrar_veiculo(placa, crlv, fotoCNH, corVeiculo, modeloVeiculo, anoVeiculo, renavam, numeroChassi):
    try:
        # Verificar se os campos obrigatórios foram preenchidos
        if not placa.strip() or not crlv.strip() or not fotoCNH.strip() or not corVeiculo.strip() or not modeloVeiculo.strip() or not anoVeiculo.strip() or not renavam.strip() or not numeroChassi.strip():
            raise ValueError("Campos obrigatórios em falta")
        
        # Conectar ao banco de dados PostgreSQ
        conn = psycopg2.connect(database="itaxi", user="postgres", password="1234", host="localhost", port="5432")
        cursor = conn.cursor()

         # Verificar se o veículo já está cadastrado, com aquela placa
        cursor.execute("SELECT * FROM veiculos WHERE placa=%s", (placa,))
        veiculo = cursor.fetchone()

        if veiculo is None:
            # Inserir novo veiculo no banco de dados
            cursor.execute("INSERT INTO veiculos (cnh, renavam, chassi, cor) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                           (placa, crlv, fotoCNH, corVeiculo, modeloVeiculo, anoVeiculo, renavam, numeroChassi))
            conn.commit()
            
            print(f"Veículo de placa: {placa} cadastrado com sucesso!")
        else:
            print(f"Veículo com placa: {placa} já está cadastrado!")

        cursor.close()
        conn.close()
        
    except ValueError as e:
        print(f"Erro ao cadastrar este veículo: {e}")

    except psycopg2.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")

    except Exception as e:
        print(f"Erro inesperado ao cadastrar o veículo: {e}")

def solicitar_corrida(usuario, origem, destino):
    try:
        method_frame, header_frame, body = channel.basic_get(queue='fila_solicitar_corrida')
        if not origem.strip() or not destino.strip():
            raise ValueError("Origem e Destino não definidos! Por favor, inserir os campos.")
    except Exception as e:
        print(f"Erro inesperado ao solicitar corrida: {e}")

def iniciar_corrida(usuario, motorista)   :
    corrida_em_andamento = None

    if corrida_em_andamento is not None:
        print("Já existe uma corrida em andamento.")
    else:
        corrida_em_andamento = {"passageiro": usuario, "motorista": motorista}
        print("f'A corrida foi iniciada. Passageiro: {usuario}, Motorista: {motorista}'")



def callback_cadastrar_usuario(ch, method, properties, body):
    mensagem = body.decode('utf-8')
    nome, email, telefone, senha, endereco, sexo = mensagem.split(';')
    senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())

    try:
        cadastrar_usuario(nome, email, telefone, senha, endereco, sexo)
    except Exception as e:
        print(f"Erro ao processar mensagem: {e}")

def callback_cadastrar_veiculo(ch, method, properties, body):
    mensagem = body.decode('utf-8')
    placa, crlv, fotoCNH, corVeiculo, modeloVeiculo, anoVeiculo, renavam, numeroChassi = mensagem.split(';')

    try:
        cadastrar_veiculo(placa, crlv, fotoCNH, corVeiculo, modeloVeiculo, anoVeiculo, renavam, numeroChassi)
    except Exception as e:
        print(f"Erro ao processar mensagem: {e}")

def callback_solicitar_corrida(ch, method, properties, body):
    mensagem = body.decode('utf-8')
    usuario, origem, destino = mensagem.split(';')

    try:
        solicitar_corrida(usuario, origem, destino)
    except Exception as e:
        print(f"Erro ao processar mensagem: {e}")

def callback_iniciar_corrida(ch, method, properties, body):
    mensagem = body.decode('utf-8')
    motorista = mensagem.split(';')

    try:
        iniciar_corrida(motorista)
    except Exception as e:
        print(f"Erro ao processar mensagem: {e}")

# Conectar ao RabbitMQ
try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
    channel = connection.channel()

    # Definir as filas a serem consumidas
    channel.queue_declare(queue='fila_cadastro')
    channel.queue_declare(queue='fila_cadastro_veiculo')
    channel.queue_declare(queue='fila_solicitar_corrida')
    channel.queue_declare(queue='fila_iniciar_corrida')

    # Configurar o callback para receber as mensagens
    channel.basic_consume(queue='fila_cadastro', on_message_callback=callback_cadastrar_usuario, auto_ack=True)
    channel.basic_consume(queue='fila_cadastro_veiculo', on_message_callback=callback_cadastrar_veiculo, auto_ack=True)
    channel.basic_consume(queue='fila_solicitar_corrida', on_message_callback=callback_solicitar_corrida, auto_ack=True)
    channel.basic_consume(queue='fila_iniciar_corrida', on_message_callback=callback_iniciar_corrida, auto_ack=True)

    print('Aguardando mensagens...')
    channel.start_consuming()
except pika.exceptions.AMQPError as e:
    print(f"Erro ao conectar ao RabbitMQ: {e}")
except Exception as e:
    print(f"Erro inesperado: {e}")
finally:
    # Certifique-se de fechar a conexão, independentemente de ocorrer uma exceção ou não
    if connection is not None and not connection.is_closed:
        connection.close()  