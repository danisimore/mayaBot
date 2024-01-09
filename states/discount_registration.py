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
