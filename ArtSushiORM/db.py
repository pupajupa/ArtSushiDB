import psycopg2
# Функция подключения к базе данных
def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname="sushi_shop",
            user="pupajupa",
            password="1234",
            host="localhost",
            port="5432"
        )
        print("Успешное подключение к базе данных!")
        return conn
    except Exception as e:
        print("Ошибка подключения к базе данных:", e)
        return None
