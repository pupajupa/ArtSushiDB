import re
# Проверка валидности данных пользователя
def validate_user_data(username, email, password, phone, first_name, last_name, address):
    errors = []
    if not username or len(username) < 3:
        errors.append("Логин должен содержать не менее 3 символов.")
    if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
        errors.append("Некорректный формат email(aboba@example.com).")
    if not password or len(password) < 6:
        errors.append("Пароль должен содержать не менее 6 символов.")
    if not phone or len(phone) < 13 or phone[0] != '+':
        errors.append("Некорректный формат номера телефона(+375290000000).")
    if not first_name or not first_name.isalpha():
        errors.append("Имя должно содержать только буквы.")
    if not last_name or not last_name.isalpha():
        errors.append("Фамилия должна содержать только буквы.")
    if not address or len(address) < 5:
        errors.append("Адрес должен содержать не менее 5 символов.")
    return errors