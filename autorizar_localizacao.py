import pika

def solicitar_autorizacao(email, aceita_permissao):
    mensagem = f"{email};{aceita_permissao}"

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
    channel = connection.channel()
    
    channel.basic_publish(exchange='', routing_key='fila_autorizar_localizacao', body=mensagem)

    print(f"Mensagem enviada: {mensagem}")

    connection.close()

# Exemplo de uso da função
solicitar_autorizacao('wandersonsousa489@gmail.com', 'sim')  # Simulando a aceitação da permissão
solicitar_autorizacao('wandersonsousa489@gmail.com', 'nao')  # Simulando a aceitação da permissão
