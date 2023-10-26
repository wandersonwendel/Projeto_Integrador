import pika
import psycopg2
import bcrypt
import geocoder

def cadastrar_passageiro(nome, email, telefone, senha, endereco, sexo):
    # Conectar ao banco de dados

    try:
        if not nome.strip() or not email.strip() or not telefone.strip() or not senha.strip():
            raise ValueError("Campos obrigatórios em falta")
        
        # Conectar ao banco de dados
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

def cadastrar_mototaxi(nome, email, telefone, senha, endereco, sexo):
    # Conectar ao banco de dados  
    try:
        if not nome.strip() or not email.strip() or not telefone.strip() or not senha.strip():
            raise ValueError("Campos obrigatórios em falta")
        
        # Conectar ao banco de dados
        conn = psycopg2.connect(database="itaxi", user="postgres", password="1234", host="localhost", port="5432")
        cursor = conn.cursor()

         # Verificar se o usuário já está cadastrado
        cursor.execute("SELECT * FROM mototaxistas WHERE email=%s", (email,))
        mototaxi = cursor.fetchone()

        if mototaxi is None:
            # Inserir novo usuário no banco de dados
            cursor.execute("INSERT INTO mototaxistas (nome, email, telefone, senha, endereco, sexo) VALUES (%s, %s, %s, %s, %s, %s)",
                           (nome, email, telefone, senha, endereco, sexo))
            conn.commit()
            
            print(f"Mototaxi {email} cadastrado com sucesso!")
        else:
            print(f"Mototaxi com o email {email} já está cadastrado!")

        cursor.close()
        conn.close()

    except ValueError as e:
        print(f"Erro ao cadastrar mototaxi: {e}")

    except psycopg2.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")

    except Exception as e:
        print(f"Erro inesperado ao cadastrar mototaxi: {e}")

def login(email, senha):
    try:
        if not email.strip() or not senha.strip():
            raise ValueError("Campos obrigatórios em falta")
    
        conn = psycopg2.connect(database="itaxi", user="postgres", password="1234", host="localhost", port="5432")
        cursor = conn.cursor()

         # Verificar se o usuário já está cadastrado
        cursor.execute("SELECT * FROM usuarios OR mototaxistas WHERE email=%s AND senha=%s", (email, senha,))
        usuario, mototaxi = cursor.fetchone()

        if usuario is None:
            print(f"Usuário {email} inexistente.")
        else:
            print(f"Usuário {email} logado com sucesso!")

        if mototaxi is None:
            print(f"Mototaxi {email} inexistente.")
        else:
            print(f"Mototaxi {email} logado com sucesso!")

        cursor.close()
        conn.close()

    except ValueError as e:
        print(f"Erro ao validar este usuário: {e}")

    except psycopg2.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")

    except Exception as e:
        print(f"Erro inesperado ao validar usuário: {e}")

def logout(email):
    pass

def autorizar_localizacao(email, aceita_permissao):
    try:
        # Conectar ao banco de dados PostgreSQL
        conn = psycopg2.connect(database="itaxi", user="postgres", password="1234", host="localhost", port="5432")
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
        conn = psycopg2.connect(database="itaxi", user="postgres", password="1234", host="localhost", port="5432")
        cursor = conn.cursor()

         # Verificar se o veículo já está cadastrado, com aquela placa
        cursor.execute("SELECT * FROM veiculos WHERE placa=%s", (placa,))
        veiculo = cursor.fetchone()

        if veiculo is None:
            # Inserir novo veiculo no banco de dados
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
        conn = psycopg2.connect(database="itaxi", user="postgres", password="1234", host="localhost", port="5432")
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

def iniciar_corrida(local_origem, destino, tempo_estimado):
    try:
        motorista_logado = True  # Substitua pelo valor real de verificação do motorista logado
        corrida_aceita = True  # Substitua pelo valor real de verificação de corrida aceita

        if motorista_logado and corrida_aceita:
            if checa_localizacao(local_origem):
                conn = psycopg2.connect(database="itaxi", user="postgres", password="1234", host="localhost", port="5432")
                cursor = conn.cursor()

                # Exibir informações no GPS
                print(f"No GPS: Destino - {destino}, Tempo estimado de viagem: {tempo_estimado}")

                cursor.close()
                conn.close()

    except ValueError as e:
        print(f"Erro ao iniciar corrida: {e}")

    except psycopg2.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")

    except Exception as e:
        print(f"Erro inesperado ao iniciar corrida: {e}")

def checar_localizacao(local_origem):
    # Lógica para checar se o motorista está no local de origem
    # Implemente sua lógica aqui. Por exemplo, você pode verificar a localização do motorista através de coordenadas GPS.
    return True  # Retornando True como exemplo

def excluir_conta(email, senha):
    try:
        if not email.strip() or not senha.strip():
            raise ValueError("Campos obrigatórios em falta")

        # Conectar ao banco de dados
        conn = psycopg2.connect(database="itaxi", user="postgres", password="1234", host="localhost", port="5432")
        cursor = conn.cursor()

        # Verificar se o usuário existe e se a senha está correta
        cursor.execute("SELECT * FROM usuarios WHERE email=%s", (email,))
        usuario = cursor.fetchone()

        if usuario:
            cursor.execute("DELETE FROM usuarios WHERE email=%s", (email,))
            conn.commit()
            print(f"Conta do usuário {email} excluída com sucesso!")
        else:
            print("Usuário não encontrado. A conta não foi excluída.")

        cursor.close()
        conn.close()

    except ValueError as e:
        print(f"Erro ao excluir conta: {e}")

    except psycopg2.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")

    except Exception as e:
        print(f"Erro inesperado ao excluir conta: {e}")

def callback_cadastrar_passageiro(ch, method, properties, body):
    mensagem = body.decode('utf-8')
    nome, email, telefone, senha, endereco, sexo = mensagem.split(';')
    senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())

    try:
        cadastrar_passageiro(nome, email, telefone, senha, endereco, sexo)
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

def callback_iniciar_corrida(ch, method, properties, body):
    # Processar a mensagem recebida e extrair os detalhes necessários
    message = body.decode('utf-8')
    dados = message.split(';')

    if dados[0] == "SOLICITACAO":
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

    """ email, mototaxi, corrida_aceita, localizacao_atual, origem, destino = message.split(';')
    try:
        iniciar_corrida(email, mototaxi, corrida_aceita, localizacao_atual, origem, destino)
    except Exception as e:
        print(f"Erro ao processar mensagem: {e}") """

def callback_excluir_conta(ch, method, properties, body):
    mensagem = body.decode('utf-8')
    email, senha = mensagem.split(';')

    try:
        excluir_conta(email, senha)
    except Exception as e:
        print(f"Erro ao processar mensagem de exclusão de conta: {e}")

def callback_logout(ch, method, properties, body):
    pass

# Conectar ao RabbitMQ
try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
    channel = connection.channel()

    # Definir as filas a serem consumidas
    channel.queue_declare(queue='fila_cadastrar_passageiro')
    channel.queue_declare(queue='fila_cadastro_veiculo')
    channel.queue_declare(queue='fila_login')
    channel.queue_declare(queue='fila_solicitar_corrida')
    channel.queue_declare(queue='fila_autorizar_localizacao')
    channel.queue_declare(queue='fila_vincular_cartao')
    channel.queue_declare(queue='fila_desvincular_cartao')
    channel.queue_declare(queue='fila_iniciar_corrida')
    channel.queue_declare(queue='fila_excluir_conta')

    # Configurar o callback para receber as mensagens
    channel.basic_consume(queue='fila_cadastrar_passageiro', on_message_callback=callback_cadastrar_passageiro, auto_ack=True)
    channel.basic_consume(queue='fila_cadastro_veiculo', on_message_callback=callback_cadastrar_veiculo, auto_ack=True)
    channel.basic_consume(queue='fila_login', on_message_callback=callback_login, auto_ack=True)
    channel.basic_consume(queue='fila_solicitar_corrida', on_message_callback=callback_solicitar_corrida, auto_ack=True)
    channel.basic_consume(queue='fila_autorizar_localizacao', on_message_callback=callback_autorizar_localizacao, auto_ack=True)
    channel.basic_consume(queue='fila_vincular_cartao', on_message_callback=callback_vincular_cartao, auto_ack=True)
    channel.basic_consume(queue='fila_desvincular_cartao', on_message_callback=callback_desvincular_cartao, auto_ack=True)
    channel.basic_consume(queue='fila_iniciar_corrida', on_message_callback=callback_iniciar_corrida, auto_ack=True)
    channel.basic_consume(queue='fila_excluir_conta', on_message_callback=callback_iniciar_corrida, auto_ack=True)

    print('Aguardando mensagens...')
    channel.start_consuming()
except pika.exceptions.AMQPError as e:
    print(f"Erro ao conectar ao RabbitMQ: {e}")
except Exception as e:
    print(f"Erro inesperado: {e}")

    connection.close()