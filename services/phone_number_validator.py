import re


def phone_num_validator(phone_number) -> bool:
    """
    Валидатор номера телефона.

    :param phone_number: номер телефона;
    :return: True если номер телефона соответствует регулярному выражению
    """
    result = re.match(
        r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$',
        phone_number
    )

    return bool(result)
