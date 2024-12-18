from db import connect_to_db
from menu import main_menu
if __name__ == "__main__":
    connection = connect_to_db()
    if connection:
        main_menu(connection)
        connection.close()
