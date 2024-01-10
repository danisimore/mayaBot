"""
Модуль для извлечения информации о пользователе из БД.

Автор: danisimore
Дата: 10.01.2024

Функция реализованная в данном модуле возвращает True, если такой username уже записан в таблице, иначе False.
На основе возвращаемого выражения, далее ограничивается возможность пользователя пройти повторную регистрацию
в дисконтной программе.
"""

import sqlite3


def select_user_data(username: str) -> bool:
    """
    Делает выборку данных о пользователе из БД.

    :param username: telegram username;
    :return:
    """

    connection = sqlite3.connect("clients.db")
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM Clients WHERE username LIKE ?', (username,))

    clients = cursor.fetchall()

    connection.commit()
    connection.close()

    return True if clients else False
