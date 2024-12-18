from validator import validate_user_data

# Функция отображения пользователей и заказов
def view_orders_and_users(conn):
    try:
        with conn.cursor() as cur:
            # Просмотр всех заказов
            cur.execute("SELECT * FROM \"Order\";")
            orders = cur.fetchall()
            print("Заказы:")
            for order in orders:
                print(f"ID Заказа: {order[0]}, ID Корзины: {order[1]}, К оплате: {order[3]}, Адрес: {order[4]}")
            
            # Просмотр всех пользователей
            cur.execute("SELECT * FROM Users;")
            users = cur.fetchall()
            print("Пользователи:")
            for user in users:
                print(f"ID Пользователя: {user[0]}, Имя: {user[5]}, Email: {user[3]}, Телефон: {user[4]}")
    except Exception as e:
        print("Ошибка при просмотре заказов и пользователей:", e)

# Функция отображения товаров
def show_products(conn):
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, price, category_id FROM product;")
            products = cur.fetchall()
            print("\nСписок товаров:")
            for product in products:
                print(f"ID: {product[0]}, Название: {product[1]}, Цена: {product[2]}, ID Категории: {product[3]}")
    except Exception as e:
        print("Ошибка выполнения запроса:", e)

# Функция отображения категорий
def show_categories(conn):
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, description FROM category;")
            categories = cur.fetchall()
            print("\nСписок категорий:")
            for category in categories:
                print(f"ID: {category[0]}, Название: {category[1]}, Описание: {category[2]}")
    except Exception as e:
        print("Ошибка выполнения запроса:", e)

# Функция добавления новой категории
def add_category(conn):
    try:
        name = input("Введите название категории: ")
        description = input("Введите описание категории: ")
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO category (name, description) VALUES (%s, %s) RETURNING id;",
                (name, description)
            )
            category_id = cur.fetchone()[0]
            conn.commit()
            print(f"Категория успешно добавлена с ID: {category_id}")
    except Exception as e:
        print("Ошибка добавления категории:", e)

def create_user(conn):
    try:
        username = input("Введите логин пользователя: ")
        email = input("Введите email пользователя: ")
        password = input("Введите пароль пользователя: ")
        phone = input("Введите номер телефона пользователя: ")
        first_name = input("Введите имя пользователя: ")
        last_name = input("Введите фамилию пользователя: ")
        address = input("Введите адрес пользователя: ")
        while True:
            role_id = input('Выберите роль(1 - admin, 2 - user): ')
            if role_id == '1':
                role_id = 1
                break
            elif role_id == '2':
                role_id = 2
                break
            else:
                print('Неверный выбор. Попробуйте ещё раз.')
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
                (username, email, password, phone, first_name, last_name, address, role_id)  # 2 - Роль "обычный пользователь"
            )
            user_id = cur.fetchone()[0]
            conn.commit()
            print(f"Пользователь успешно зарегистрирован с ID: {user_id}")
    except Exception as e:
        print("Ошибка регистрации пользователя:", e)

def update_user(conn):
    try:
        with conn.cursor() as cur:
            user_id = int(input("Введите ID пользователя для обновления: "))
            email = input("Введите новый email: ")
            phone = input("Введите новый номер телефона: ")
            first_name = input("Введите новое имя: ")
            last_name = input("Введите новую фамилию: ")
            address = input("Введите новый адрес: ")
            if email:
                cur.execute("UPDATE Users SET email = %s WHERE id = %s;", (email, user_id))
            if phone:
                cur.execute("UPDATE Users SET phone = %s WHERE id = %s;", (phone, user_id))
            if first_name:
                cur.execute("UPDATE Users SET first_name = %s WHERE id = %s;", (first_name, user_id))
            if last_name:
                cur.execute("UPDATE Users SET last_name = %s WHERE id = %s;", (last_name, user_id))
            if address:
                cur.execute("UPDATE Users SET address = %s WHERE id = %s;", (address, user_id))

            conn.commit()

            print("Данные пользователя обновлены.")
    except Exception as e:
        print("Ошибка при обновлении пользователя:", e)

def delete_user(conn):
    try:
        with conn.cursor() as cur:
            user_id = int(input("Введите ID пользователя для удаления: "))
            cur.execute("DELETE FROM Users WHERE id = %s;", (user_id,))
            conn.commit()
            print("Пользователь удален.")
    except Exception as e:
        print("Ошибка при удалении пользователя:", e)

def add_product(conn):
    try:
        with conn.cursor() as cur:
            category_id = int(input("Введите ID категории товара: "))
            name = input("Введите название товара: ")
            description = input("Введите описание товара: ")
            price = float(input("Введите цену товара: "))
            image_url = input("Введите URL изображения товара: ")

            cur.execute("INSERT INTO Product (category_id, name, description, price, image_url) VALUES (%s, %s, %s, %s, %s);", 
                        (category_id, name, description, price, image_url))
            conn.commit()
            print("Товар добавлен.")
    except Exception as e:
        print("Ошибка при добавлении товара:", e)

def update_product(conn):
    try:
        with conn.cursor() as cur:
            product_id = int(input("Введите ID товара для обновления: "))
            name = input("Введите новое название товара (оставьте пустым, если не нужно менять): ")
            description = input("Введите новое описание товара (оставьте пустым, если не нужно менять): ")
            price = input("Введите новую цену товара (оставьте пустым, если не нужно менять): ")
            image_url = input("Введите новый URL изображения товара (оставьте пустым, если не нужно менять): ")

            if name:
                cur.execute("UPDATE Product SET name = %s WHERE id = %s;", (name, product_id))
            if description:
                cur.execute("UPDATE Product SET description = %s WHERE id = %s;", (description, product_id))
            if price:
                cur.execute("UPDATE Product SET price = %s WHERE id = %s;", (price, product_id))
            if image_url:
                cur.execute("UPDATE Product SET image_url = %s WHERE id = %s;", (image_url, product_id))

            conn.commit()
            print("Товар обновлен.")
    except Exception as e:
        print("Ошибка при обновлении товара:", e)

def delete_product(conn):
    try:
        with conn.cursor() as cur:
            product_id = int(input("Введите ID товара для удаления: "))
            cur.execute("DELETE FROM Product WHERE id = %s;", (product_id,))
            conn.commit()
            print("Товар удален.")
    except Exception as e:
        print("Ошибка при удалении товара:", e)

def view_user_log(conn):
    try:
        with conn.cursor() as cur:
            # Получаем все записи из журнала действий, сортируя по времени
            cur.execute("SELECT * FROM UserLog ORDER BY log_time DESC;")
            logs = cur.fetchall()

            if not logs:
                print("Журнал действий пуст.")
                return

            print("Журнал действий:")
            for log in logs:
                print(f"ID: {log[0]}, Пользователь ID: {log[1]}, Действие: {log[2]}, "
                      f"IP адрес: {log[4]}, Время: {log[3]}")
    except Exception as e:
        print("Ошибка при просмотре журнала действий:", e)