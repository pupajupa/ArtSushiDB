from authorization import login_user,register_user
from admin_menu import admin_menu
from user_menu import user_menu

# Главное меню приложения
def main_menu(conn):
    while True:
        print("\n--- Главное меню ---")
        print("1. Войти в аккаунт")
        print("2. Зарегистрироваться")
        print("3. Выйти")
        choice = input("Выберите действие: ")

        if choice == "1":
            user = login_user(conn)
            if user:
                if user["role_id"] == 1:  # 1 - Роль "администратор"
                    admin_menu(conn, user)
                else:
                    user_menu(conn, user)
        elif choice == "2":
            register_user(conn)
        elif choice == "3":
            print("Выход из приложения.")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")