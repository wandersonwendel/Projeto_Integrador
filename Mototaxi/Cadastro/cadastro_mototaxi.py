import psycopg2

def verificar_mototaxi_existente(email):
    conn = psycopg2.connect(database="itaxi", user="postgres", password="1234", host="localhost", port="5432")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM mototaxis WHERE email=%s", (email,))
    count = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return count > 0

def cadastrar_mototaxi(email, latitude, longitude, disponivel):
    try:
        # Verificar se o CPF já existe
        if verificar_mototaxi_existente(email):
            print(f"Um entregador com o CPF {email} já está cadastrado.")
            # Aqui você pode escolher entre atualizar os dados existentes ou exibir uma mensagem de erro
            return

        # Conectar ao banco de dados PostgreSQL
        conn = psycopg2.connect(database="itaxi", user="postgres", password="1234", host="localhost", port="5432")
        cursor = conn.cursor()

        # Inserir novo entregador no banco de dados
        cursor.execute("INSERT INTO entregadores (email, latitude, longitude, disponivel) VALUES (%s, %s, %s, %s)",
                       (email, latitude, longitude, disponivel))
        conn.commit()

        print(f"Entregador {email} cadastrado com sucesso!")

        cursor.close()
        conn.close()

    except psycopg2.Error as e:
        print(f"Ocorreu um erro ao acessar o banco de dados: {e}")

# Exemplo de uso
cadastrar_mototaxi('ari@gmail.com', 15, 1, True)
