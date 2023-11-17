import pika

def logout_passageiro(email):
    mensagem = email

    try:
        # Conectar ao RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672)) 
        channel = connection.channel() 

        # Publicar a mensagem na fila
        channel.basic_publish(exchange='', routing_key='fila_logout_passageiro', body=mensagem)

        print(f'Mensagem de logout enviada para o passageiro: {email}')

    except pika.exceptions.AMQPError as e:
        print(f"Erro ao conectar ao RabbitMQ: {e}")

    except Exception as e:
        print(f"Erro inesperado ao enviar mensagem de logout: {e}")

    finally:
        # Certifique-se de fechar a conexão, mesmo em caso de erro
        connection.close()

# Exemplo de uso
logout_passageiro('wandersonsousa489@gmail.com')