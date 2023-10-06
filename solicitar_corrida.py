import pika

try:
    # Configuração da conexão com o RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declarar uma fila para as solicitações de corrida
    channel.queue_declare(queue='solicitacoes_corrida')

    def solicitar_corrida(usuario, origem, destino):
        try:
            # Enviar a solicitação de corrida para a fila
            message = f'Solicitação de corrida: {usuario}, de {origem} para {destino}'
            channel.basic_publish(exchange='', routing_key='solicitacoes_corrida', body=message)
            print(f'Solicitação de corrida enviada: {message}')
        except Exception as e:
            print(f"Erro ao enviar a solicitação de corrida: {e}")

    def iniciar_corrida(motorista):
        try:
            # Simular um motorista aceitando a corrida
            method_frame, header_frame, body = channel.basic_get(queue='solicitacoes_corrida')
            if body:
                print(f'Motorista {motorista} aceitou a corrida: {body}')
            else:
                print('Nenhuma corrida disponível.')
        except Exception as e:
            print(f"Erro ao iniciar a corrida: {e}")
        finally:
            # Fechar a conexão com o RabbitMQ
            connection.close()

    # Exemplo de uso
    solicitar_corrida('João', 'Aeroporto', 'Hotel')
    solicitar_corrida('Maria', 'Estação de trem', 'Restaurante')

    # Simular um motorista aceitando a corrida
    iniciar_corrida('Motorista1')

except Exception as e:
    print(f"Erro ao configurar a conexão com o RabbitMQ: {e}")
