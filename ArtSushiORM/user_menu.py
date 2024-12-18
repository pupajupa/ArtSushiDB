from user import *

# Главное меню пользователя
def user_menu(conn, user):
    while True:
        print("\n--- Меню пользователя ---")
        print("1. Просмотреть товары")
        print("2. Добавить товар в корзину")
        print("3. Оформить заказ")
        print("4. Просмотреть историю заказов")
        print("5. Редактировать профиль")
        print("6. Оставить отзыв")
        print("7. Редактировать свой отзыв")
        print("8. Выйти из аккаунта")
        choice = input("Выберите действие: ")

        if choice == "1":
            show_products(conn)
        elif choice == "2":
            add_to_cart(conn, user["id"])
        elif choice == "3":
            place_order(conn, user["id"])
        elif choice == "4":
            view_order_history(conn, user["id"])
        elif choice == "5":
            edit_profile(conn, user["id"])
        elif choice == "6":
            product_id = int(input("Введите ID товара: "))
            leave_review(conn, user["id"], product_id)
        elif choice == "7":
            product_id = int(input("Введите ID товара для редактирования отзыва: "))
            edit_review(conn, user["id"], product_id)
        elif choice == "8":
            print("Выход из аккаунта.")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")