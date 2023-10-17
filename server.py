import pika
import psycopg2
import bcrypt
import geocoder

def cadastrar_usuario(nome, email, telefone, senha, endereco, sexo):
    # Conectar ao banco de dados PostgreSQ
    try:
        if not nome.strip() or not email.strip() or not telefone.strip() or not senha.strip():
            raise ValueError("Campos obrigatórios em falta")
        
        # Conectar ao banco de dados
        conn = psycopg2.connect(database="itaxi", user="postgres", password="1234", host="192.168.3.6", port="5432")
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

def login(email, senha):
    try:
        if not email.strip() or not senha.strip():
            raise ValueError("Campos obrigatórios em falta")
        
        # Resto do código de cadastro aqui
        conn = psycopg2.connect(database="itaxi", user="postgres", password="1234", host="192.168.3.6", port="5432")
        cursor = conn.cursor()

         # Verificar se o usuário já está cadastrado
        cursor.execute("SELECT * FROM usuarios WHERE email=%s", (email,))
        usuario = cursor.fetchone()

        if usuario is None:
            print(f"Usuário {email} inexistente.")
        else:
            print(f"Usuário {email} logado com sucesso!")

        cursor.close()
        conn.close()

    except ValueError as e:
        print(f"Erro ao validar este usuário: {e}")

    except psycopg2.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")

    except Exception as e:
        print(f"Erro inesperado ao validar usuário: {e}")


def autorizar_localizacao(email, aceita_permissao):
    try:
        # Conectar ao banco de dados PostgreSQL
        conn = psycopg2.connect(database="itaxi", user="postgres", password="1234", host="192.168.3.6", port="5432")
        cursor = conn.cursor()

        # Verificar se o usuário está devidamente logado no sistema
        cursor.execute("SELECT * FROM usuarios WHERE email=%s", (email,))
        usuario = cursor.fetchone()

        if aceita_permissao == "sim":
            print("Permissão concedida. Obtendo a localização atual e exibindo no mapa.")
         
            g = geocoder.ip('me')
            localizacao = g.latlng  # Isso irá retornar uma tupla com a latitude e longitude
        
            if localizacao:
                latitude, longitude = localizacao
                print(f"Sua localização é: Latitude {latitude}, Longitude {longitude}")
            else:
                print("Não foi possível obter a localização.")
        elif aceita_permissao == 'nao':
            print("Você negou o acesso à localização.")
        else:
            print("Erro")
        

        cursor.close()
        conn.close()

    except psycopg2.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")

    except Exception as e:
        print(f"Erro inesperado ao autorizar localização: {e}")


def cadastrar_veiculo(placa, crlv, fotoCNH, corVeiculo, modeloVeiculo, anoVeiculo, renavam, numeroChassi):
    try:
        # Verificar se os campos obrigatórios foram preenchidos
        if not placa.strip() or not crlv.strip() or not fotoCNH.strip() or not corVeiculo.strip() or not modeloVeiculo.strip() or not anoVeiculo.strip() or not renavam.strip() or not numeroChassi.strip():
            raise ValueError("Campos obrigatórios em falta")
        
        # Conectar ao banco de dados
        conn = psycopg2.connect(database="itaxi", user="postgres", password="1234", host="192.168.3.6", port="5432")
        cursor = conn.cursor()

         # Verificar se o veículo já está cadastrado, com aquela placa
        cursor.execute("SELECT * FROM veiculos WHERE placa=%s", (placa,))
        veiculo = cursor.fetchone()

        if veiculo is None:
            # Inserir novo veiculo no banco de dados
            cursor.execute("INSERT INTO veiculos (placa, crlv, fotoCNH, corVeiculo, modeloVeiculo, anoVeiculo, renavam, numeroChassi) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            cursor.execute("INSERT INTO veiculos (placa, crlv, fotoCNH, corVeiculo, modeloVeiculo, anoVeiculo, renavam, numeroChassi) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
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

def solicitar_corrida(email, endereco, endereco_destino):
    try:
        # Conectar ao banco de dados
        conn = psycopg2.connect(database="itaxi", user="postgres", password="1234", host="192.168.3.6", port="5432")
        cursor = conn.cursor()

         # Verificar se o usuário já está cadastrado
        cursor.execute("SELECT * FROM usuarios WHERE email=%s And endereco=%s", (email, endereco,))
        email= cursor.fetchone()

        valor_corrida = 5.00

        if endereco is None:
            print(f"Endereço de origem: {endereco} não cadastrato em nossa base de dados!.")
        else:
            print(f"Corrida solicitada! Origem: {endereco}, Destino: {endereco_destino}. Valor da corrida: {valor_corrida}")

        cursor.close()
        conn.close()

    except ValueError as e:
        print(f"Erro ao validar este usuário: {e}")

    except psycopg2.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")

    except Exception as e:
        print(f"Erro inesperado ao validar usuário: {e}")


def vincular_cartao(email, numero_cartao, nome_titular, data_validade, cvv):
    try:
        conn = psycopg2.connect(database="itaxi", user="postgres", password="1234", host="localhost", port="5432")
        cursor = conn.cursor()

        # Verificar se o usuário existe no banco de dados
        cursor.execute("SELECT * FROM usuarios WHERE email=%s", (email,))
        usuario = cursor.fetchone()

        if usuario:
            # Inserir os detalhes do cartão no banco de dados do usuário
            cursor.execute("INSERT INTO cartoes (email, numero_cartao, nome_titular, data_validade, cvv) VALUES (%s, %s, %s, %s, %s)",
            cursor.execute("INSERT INTO cartoes (email, numero_cartao, nome_titular, data_validade, cvv) VALUES (%s, %s, %s, %s, %s)",
                           (email, numero_cartao, nome_titular, data_validade, cvv))
            conn.commit()

            print("Cartão vinculado com sucesso.")
        else:
            print("Usuário não encontrado.")

        cursor.close()
        conn.close()

    except psycopg2.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")

    except Exception as e:
        print(f"Erro inesperado ao vincular o cartão: {e}")

def desvincular_cartao(email, numero_cartao):
    try:
        conn = psycopg2.connect(database="itaxi", user="postgres", password="1234", host="localhost", port="5432")
        cursor = conn.cursor()

        # Verificar se o usuário possui o cartão no banco de dados
        cursor.execute("SELECT * FROM cartoes WHERE email=%s AND numero_cartao=%s", (email, numero_cartao))
        cartao = cursor.fetchone()

        if cartao:
            # Remover o cartão do banco de dados
            cursor.execute("DELETE FROM cartoes WHERE email=%s AND numero_cartao=%s", (email, numero_cartao))
            conn.commit()

            print("Cartão desvinculado com sucesso.")
        else:
            print("Cartão não encontrado para este usuário.")

        cursor.close()
        conn.close()

    except psycopg2.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")

    except Exception as e:
        print(f"Erro inesperado ao desvincular o cartão: {e}")



def callback_cadastrar_usuario(ch, method, properties, body):
    mensagem = body.decode('utf-8')
    nome, email, telefone, senha, endereco, sexo = mensagem.split(';')
    senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())

    try:
        cadastrar_usuario(nome, email, telefone, senha, endereco, sexo)
    except Exception as e:
        print(f"Erro ao processar mensagem: {e}")

def callback_login(ch, method, properties, body):
    mensagem = body.decode('utf-8')
    email, senha = mensagem.split(';')
    senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())

    try:
        login(email, senha)
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
    email, endereco, endereco_destino = mensagem.split(';')

    try:
        solicitar_corrida(email, endereco, endereco_destino)
    except Exception as e:
        print(f"Erro ao processar mensagem: {e}")

def callback_autorizar_localizacao(ch, method, properties, body):
    mensagem = body.decode('utf-8')
    email, aceita_permissao = mensagem.split(';')

    try:
        autorizar_localizacao(email, aceita_permissao)
    except Exception as e:
        print(f"Erro ao processar mensagem: {e}")

def callback_vincular_cartao(ch, method, properties, body):
    mensagem = body.decode()
    email, numero_cartao, nome_titular, data_validade, cvv = mensagem.split(';')

    try:
        vincular_cartao(email, numero_cartao, nome_titular, data_validade, cvv)
    except Exception as e:
        print(f"Erro ao processar mensagem: {e}")

def callback_desvincular_cartao(ch, method, properties, body):
    mensagem = body.decode()
    email, numero_cartao = mensagem.split(';')

    try:
        desvincular_cartao(email, numero_cartao)
    except Exception as e:
        print(f"Erro ao processar mensagem: {e}")

# Conectar ao RabbitMQ
try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.3.6', port=5672))
    channel = connection.channel()

    # Definir as filas a serem consumidas
    channel.queue_declare(queue='fila_cadastro')
    channel.queue_declare(queue='fila_cadastro_veiculo')
    channel.queue_declare(queue='fila_login')
    channel.queue_declare(queue='fila_solicitar_corrida')
    channel.queue_declare(queue='fila_autorizar_localizacao')
    channel.queue_declare(queue='fila_vincular_cartao')
    channel.queue_declare(queue='fila_desvincular_cartao')

    # Configurar o callback para receber as mensagens
    channel.basic_consume(queue='fila_cadastro', on_message_callback=callback_cadastrar_usuario, auto_ack=True)
    channel.basic_consume(queue='fila_cadastro_veiculo', on_message_callback=callback_cadastrar_veiculo, auto_ack=True)
    channel.basic_consume(queue='fila_login', on_message_callback=callback_login, auto_ack=True)
    channel.basic_consume(queue='fila_solicitar_corrida', on_message_callback=callback_solicitar_corrida, auto_ack=True)
    channel.basic_consume(queue='fila_autorizar_localizacao', on_message_callback=callback_autorizar_localizacao, auto_ack=True)
    channel.basic_consume(queue='fila_vincular_cartao', on_message_callback=callback_vincular_cartao, auto_ack=True)
    channel.basic_consume(queue='fila_desvincular_cartao', on_message_callback=callback_desvincular_cartao, auto_ack=True)

    print('Aguardando mensagens...')
    channel.start_consuming()
except pika.exceptions.AMQPError as e:
    print(f"Erro ao conectar ao RabbitMQ: {e}")
except Exception as e:
    print(f"Erro inesperado: {e}")

    connection.close()