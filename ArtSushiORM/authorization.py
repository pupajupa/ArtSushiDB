from validator import *

# Функция входа в систему
def login_user(conn):
    try:
        print("\n--- Вход в систему ---")
        username = input("Введите логин: ")
        password = input("Введите пароль: ")
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, role_id FROM users WHERE username = %s AND password = %s;",
                (username, password)
            )
            user = cur.fetchone()
            if user:
                print("Успешный вход!")
                return {"id": user[0], "role_id": user[1]}
            else:
                print("Неверный логин или пароль.")
                return None
    except Exception as e:
        print("Ошибка входа:", e)
        return None
    
# Функция регистрации пользователя
def register_user(conn):
    try:
        print("\n--- Регистрация пользователя ---")
        username = input("Введите логин: ")
        email = input("Введите email: ")
        password = input("Введите пароль: ")
        phone = input("Введите номер телефона:")
        first_name = input("Введите имя: ")
        last_name = input("Введите фамилию: ")
        address = input("Введите адрес: ")

        # Проверка валидности данных
        errors = validate_user_data(username, email, password, phone, first_name, last_name, address)
        if errors:
            print("\nОшибки при вводе данных:")
            for error in errors:
                print(f"- {error}")
            return

        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (username, email, password, phone, first_name, last_name, address, role_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;",
                (username, email, password, phone, first_name, last_name, address, 2)  # 2 - Роль "обычный пользователь"
            )
            user_id = cur.fetchone()[0]
            conn.commit()
            print(f"Пользователь успешно зарегистрирован с ID: {user_id}")
    except Exception as e:
        print("Ошибка регистрации пользователя:", e)