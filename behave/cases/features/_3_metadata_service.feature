Функционал: Работа с metadata-service

@metadata-service
Сценарий: Проверяем создание и поиск структур по системному имени
    Допустим в networkID "1" удаляем структуру "dog"
    Если в networkID "1" создаем структуру "dog" с полями
    """
    [
        {"sysName":"id","dataType":"id","name":"id","link":"","indexing":false,"ordering":false,"linkIndexFieldSysName":[],"arrayLink":false,"linkType":false,"linkOrArrayLinkType":false},
        {"sysName":"name","dataType":"string","name":"name","link":"","indexing":false,"ordering":false,"linkIndexFieldSysName":[],"arrayLink":false,"linkType":false,"linkOrArrayLinkType":false},
        {"sysName":"age","dataType":"number","name":"age","link":"","indexing":false,"ordering":false,"linkIndexFieldSysName":[],"arrayLink":false,"linkType":false,"linkOrArrayLinkType":false},
        {"sysName":"weight","dataType":"decimal","name":"weight","link":"","indexing":false,"ordering":false,"linkIndexFieldSysName":[],"arrayLink":false,"linkType":false,"linkOrArrayLinkType":false}
    ]
    """
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
    И в networkID "1" удаляем структуру "dog"



#FindByNetworkID
#ScenarioDirectoriesMapping
