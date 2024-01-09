from aiogram.filters import Filter
from aiogram.types import Message


class MessageTextFilter(Filter):
    """
    Класс фильтра, для проверки, соответствует ли текст сообщения пользователя требуемому тексту.
    """

    def __init__(self, my_text: str) -> None:
        """
        Инициализатор класса.

        :param my_text: переменная с текстом, с которым должен совпадать текст сообщения пользователя
        """
        self.my_text = my_text

    async def __call__(self, message: Message) -> bool:
        """
        Проверяет, совпадает ли текст из сообщения с требуемым текстом.

        :param message: сообщение пользователя
        :return: True - текст совпадает, False - нет
        """
        return message.text == self.my_text
