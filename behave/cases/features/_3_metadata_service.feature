Функционал: Работа с metadata-service

@wip
@metadata-service
Сценарий: создание тестовой структуры, добавление полей в метаинформацию
    Допустим вызываем "metadata-service.FindBySysName" и проверяем
    """
    {
        "request" : {
            "networkID" : 1,
            "sysName" : "dog"
        },
        "assert" : {
            "value" : {
                "networkID.value" : 1,
                "sysName.value" : "dog"
            }
        }
    }
    """
