import datetime

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

# Функция для добавления товара в корзину
def add_to_cart(conn, user_id):
    try:
        product_id = int(input("Введите ID товара: "))
        quantity = int(input("Введите количество: "))
        # Получаем цену товара из таблицы Product
        with conn.cursor() as cur:
            cur.execute("SELECT price FROM product WHERE id = %s;", (product_id,))
            product = cur.fetchone()
            
            if product:
                price = product[0]
            else:
                print("Товар с таким ID не найден.")
                return

        # Проверяем, есть ли у пользователя корзина
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM cart WHERE user_id = %s;", (user_id,))
            cart = cur.fetchone()

            if not cart:
                # Если корзины нет, создаем новую
                cur.execute("INSERT INTO cart (user_id) VALUES (%s) RETURNING id;", (user_id,))
                cart_id = cur.fetchone()[0]
                conn.commit()
                print(f"Создана новая корзина с ID: {cart_id}")
            else:
                cart_id = cart[0]
                print(f"Используется существующая корзина с ID: {cart_id}")

        # Добавляем товар в корзину
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO cartitem (quantity, price, cart_id, product_id) VALUES (%s, %s, %s, %s);",
                (quantity, price, cart_id, product_id)
            )
            conn.commit()
            print(f"Товар добавлен в корзину (ID товара: {product_id}, количество: {quantity}, цена: {float(price)*int(quantity)})")

    except Exception as e:
        print("Ошибка добавления товара в корзину:", e)



def place_order(conn, user_id):
    try:
        delivery_address = input("Введите адрес доставки: ")
        payment_method_id = int(input("Введите ID способа оплаты: "))
        with conn.cursor() as cur:
            # Получаем корзину пользователя
            cur.execute("SELECT id FROM cart WHERE user_id = %s;", (user_id,))
            cart = cur.fetchone()

            if not cart:
                print("У вас нет корзины.")
                return

            cart_id = cart[0]
            # Проверяем, есть ли товары в корзине
            cur.execute("""
                SELECT COUNT(*) 
                FROM cartitem ci
                WHERE ci.cart_id = %s;
            """, (cart_id,))
            item_count = cur.fetchone()[0]

            if item_count == 0:
                print("У вас нет товаров в корзине.")
                return

            # Получаем общую стоимость корзины
            cur.execute("""
                SELECT SUM(ci.quantity * p.price) 
                FROM cartitem ci
                JOIN product p ON ci.product_id = p.id
                WHERE ci.cart_id = %s;
            """, (cart_id,))

            # Вызов процедуры создания заказа
            cur.execute("CALL create_order(%s, %s, %s);", (user_id, delivery_address, payment_method_id))
            conn.commit()

            print(f"Заказ оформлен!")
    except Exception as e:
        print("Ошибка оформления заказа:", e)


def view_order_history(conn, user_id):
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT o.id, o.total_price, os.status_name, o.created_at
                FROM \"Order\" o
                JOIN orderstatus os ON o.status_id = os.id
                WHERE o.cart_id IN (SELECT id FROM cart WHERE user_id = %s);
            """, (user_id,))
            orders = cur.fetchall()

            if not orders:
                print("У вас нет заказов.")
                return

            print("\nИстория заказов:")
            for order in orders:
                print(f"ID: {order[0]}, Сумма: {order[1]}, Статус: {order[2]}, Дата: {order[3]}")
    except Exception as e:
        print("Ошибка просмотра истории заказов:", e)

def edit_profile(conn, user_id):
    try:
        print("\n--- Редактирование профиля ---")
        email = input("Введите новый email: ")
        phone = input("Введите новый номер телефона: ")
        first_name = input("Введите новое имя: ")
        last_name = input("Введите новую фамилию: ")
        address = input("Введите новый адрес: ")

        with conn.cursor() as cur:
            cur.execute("""
                UPDATE users
                SET email = %s, phone = %s, first_name = %s, last_name = %s, address = %s
                WHERE id = %s;
            """, (email, phone, first_name, last_name, address, user_id))
            conn.commit()

            print("Профиль успешно обновлен.")
    except Exception as e:
        print("Ошибка редактирования профиля:", e)

def leave_review(conn, user_id, product_id):
    try:
        now = datetime.datetime.now()
        rating = int(input("Оцените товар (1-5): "))
        comment = input("Ваш отзыв: ")
        created_at = now.strftime("%Y-%m-%d %H:%M:%S")
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO review (user_id, product_id, rating, comment, created_at) VALUES (%s, %s, %s, %s, %s);",
                (user_id, product_id, rating, comment, created_at)
            )
            conn.commit()
            print("Отзыв успешно оставлен.")
    except Exception as e:
        print("Ошибка оставления отзыва:", e)

def edit_review(conn, user_id, product_id):
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, rating, comment FROM review WHERE user_id = %s AND product_id = %s;", (user_id, product_id))
            review = cur.fetchone()

            if not review:
                print("Отзыв не найден.")
                return

            print(f"Ваш отзыв: Оценка: {review[1]}, Комментарий: {review[2]}")
            rating = int(input("Введите новую оценку (1-5): "))
            comment = input("Введите новый комментарий: ")

            cur.execute("""
                UPDATE review
                SET rating = %s, comment = %s
                WHERE id = %s;
            """, (rating, comment, review[0]))
            conn.commit()

            print("Отзыв успешно обновлен.")
    except Exception as e:
        print("Ошибка редактирования отзыва:", e)