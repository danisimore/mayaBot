from aiogram.fsm.state import StatesGroup, State


class DiscountRegistration(StatesGroup):
    """
    Состояния оформления дисконтной карты.
    """

    making_decision = State()
    entering_name = State()
