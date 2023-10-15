import geocoder

def solicitar_autorizacao(email, aceita_permissao):
    aceita_permissao = input("Você deseja permitir o acesso à sua localização? (sim/não): ")
    mensagem = f"{email};{aceita_permissao}"

    if aceita_permissao.lower() == "sim":
        print(f'Mensagem enviada: {mensagem}')
        g = geocoder.ip('me')
        localizacao = g.latlng  # Isso irá retornar uma tupla com a latitude e longitude
        
        if localizacao:
            latitude, longitude = localizacao
            print(f"Sua localização é: Latitude {latitude}, Longitude {longitude}")
        else:
            print("Não foi possível obter a localização.")
    else:
        print("Você negou o acesso à localização.")

# Exemplo de uso da função
solicitar_autorizacao('wandersonsousa489@gmail.com', True)  # Simulando a aceitação da permissão
