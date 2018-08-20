Функционал: Работа с metadata-service

@wip
@metadata-service
Сценарий: Проверяем создание и поиск структур по системному имени
    Допустим в networkID "1" удаляем структуру "dog"
    Если в networkID "1" создаем структуру "dog"
    То ищем структуру и проверяем
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



#FindByNetworkID
#ScenarioDirectoriesMapping
