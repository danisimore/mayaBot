"""
Модуль с описанием класса состояний регистрации в дисконтной программе.


Автор: danisimore
Дата: 10.01.2024


В классе состояний регистрации в дисконтной программе описаны следующие состояния:
    making_decision - состояние принятия решения, когда пользователю предлагается регистрация;
    entering_name - состояние ожидания ввода имени;
    entering_last_name - состояние ожидания ввода фамилии;
    entering_patronymic - состояние ожидания ввода отчества;
    entering_phone_number - состояние ожидания ввода номера телефона;
    checking_entered_data - состояние проверки пользователем введенных данных.
"""

from aiogram.fsm.state import StatesGroup, State


class DiscountRegistration(StatesGroup):
    """
    Состояния оформления дисконтной карты.
    """

    making_decision = State()
    entering_name = State()
    entering_last_name = State()
    entering_patronymic = State()
    entering_phone_number = State()
    checking_entered_data = State()
