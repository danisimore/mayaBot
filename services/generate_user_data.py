"""
Модуль для формирования строки с данными о пользователе, который регистрируется в дисконтной программе.


Автор: danisimore
Дата: 10.01.2024


Функция в данном модуле принимает параметр user_data - словарь с информацией о пользователе,
которую он указал в чате с ботом, в процессе регистрации в дисконтной программе. Далее формирует строку на основе
значений ключей. Возвращает эту строку.
"""


def generate_user_data(user_data: dict) -> str:
    """
    Составляет строку из словаря с данными.

    :param user_data: информация, собранная о пользователе;
    :return: str из собранной информации и отформатированная для большей читабельности
    """

    user_data_string = f"""
Имя: {user_data.get('user_entered_name')}
Фамилия: {user_data.get('user_entered_last_name')}
Отчество: {user_data.get('user_entered_patronymic')}\n
Номер телефона: {user_data.get('user_entered_phone_number')}
    """

    return user_data_string
