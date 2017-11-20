Функционал: Выдача истории изменения объекта

Сценарий: проводим ряд модификаций объекта и смотрим историю изменений
    Допустим работает шаг "Если указаны app_id и app_secret"
    И сохраняем объект структуры "dog"
    """
    {
        "id": "2",
        "dogName": "Tommy"
    }
    """
    И сохраняем объект структуры "dog"
    """
    {
        "id": "2",
        "dogName": "Tommy is not Dog"
    }
    """
    И сохраняем объект структуры "dog"
    """
    {
        "id": "2",
        "dogName": "Tommy is not Dog"
        "dogHeight": 215
    }
    # TODO модифицируем поле
    """
    То объект структуры "dog" с id "2" имеет "3" версии
    И версия с индексом 0 точно соответствует
    """
    {
        "id": "2",
        "dogName": "Tommy"
    }
    """
    И версия с индексом 1 точно соответствует
    """
    {
        "id": "2",
        "dogName": "Tommy is not Dog"
    }
    """
    И версия с индексом 2 точно соответствует
    """
    {
        "id": "2",
        "dogName": "Tommy is not Dog"
        "dogHeight": 215
    }
    """