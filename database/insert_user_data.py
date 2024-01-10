"""
Модуль для занесения информации о пользователе в БД.

Автор: danisimore
Дата: 10.01.2024

Функция реализованная в данном модуле делает запись в таблице Clients о пользователе, используя данные,
которые он указал при регистрации в дисконтной программе в боте Telegram.
"""

import sqlite3


def insert_user_data(username: str, phone_number: str) -> None:
    """
    Заносит данные о пользователе в БД.

    :param username: telegram username;
    :param phone_number: указанный пользователем номер телефона
    :return:
    """

    connection = sqlite3.connect("clients.db")
    cursor = connection.cursor()

    # Выбираем всех пользователей
    cursor.execute('INSERT INTO Clients (username, phone_number) VALUES (?, ?)', (username, phone_number))

    connection.commit()
    connection.close()

