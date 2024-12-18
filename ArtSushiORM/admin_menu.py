from admin import *

# Главное меню администратора
def admin_menu(conn, user):
    while True:
        print("\n--- Меню администратора ---")
        print("1. Просмотреть пользователей и заказы")
        print("2. Просмотреть товары")
        print("3. Просмотреть категории")
        print("4. CRUD операции с пользователями")
        print("5. CRUD операции с товарами")
        print("6. Просмотр журнала действий всех пользователей")
        print("7. Обновить статус заказа")
        print("8. Выйти из аккаунта")
        choice = input("Выберите действие: ")

        if choice == "1":
            view_orders_and_users(conn)
        elif choice == "2":
            show_products(conn)
        elif choice == "3":
            show_categories(conn)
        elif choice == "4":
            while True:
                print("Выберите действие с пользователем:")
                print("1. Создать")
                print("2. Обновить")
                print("3. Удалить")
                print("0. Назад")
                choice1 = input('Ваш выбор: ')
                if choice1 == '1':
                    create_user(conn)
                    break
                elif choice1 =='2':
                    update_user(conn)
                    break
                elif choice1 == '3':
                    delete_user(conn)
                    break
                elif choice1 == '0':
                    break
                else:
                    print('Неверный ввод. Попробуйте еще раз.')
        elif choice == "5":
            while True:
                print("Выберите действие с товаром:")
                print("1. Создать")
                print("2. Обновить")
                print("3. Удалить")
                print("0. Назад")
                choice1 = input('Ваш выбор: ')
                if choice1 == '1':
                    add_product(conn)
                    break
                elif choice1 =='2':
                    update_product(conn)
                    break
                elif choice1 == '3':
                    delete_product(conn)
                    break
                elif choice1 == '0':
                    break
                else:
                    print('Неверный ввод. Попробуйте еще раз.')
        elif choice == "6":
            view_user_log(conn)
        elif choice =="7":
            call_update_order_status(conn)
        elif choice == "8":
            print("Выход из аккаунта.")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")