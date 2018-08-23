Функционал: Работа с mongodb-service

@wip
@metadata-service
@mongodb-service
Сценарий: Проверяем добавление и поиск данных
    Допустим в networkID "1" удаляем структуру "dog"
    И в networkID "1" создаем структуру "dog" с полями
    """
    [
        {"sysName":"id","dataType":"id","name":"id","link":"","indexing":false,"ordering":false,"linkIndexFieldSysName":[],"arrayLink":false,"linkType":false,"linkOrArrayLinkType":false},
        {"sysName":"name","dataType":"string","name":"name","link":"","indexing":false,"ordering":false,"linkIndexFieldSysName":[],"arrayLink":false,"linkType":false,"linkOrArrayLinkType":false},
        {"sysName":"age","dataType":"number","name":"age","link":"","indexing":false,"ordering":false,"linkIndexFieldSysName":[],"arrayLink":false,"linkType":false,"linkOrArrayLinkType":false},
        {"sysName":"weight","dataType":"decimal","name":"weight","link":"","indexing":false,"ordering":false,"linkIndexFieldSysName":[],"arrayLink":false,"linkType":false,"linkOrArrayLinkType":false}
    ]
    """
    То в networkID "1" создаем объект в структуре "dog"
    """
    {
        "request" : {
            "id" : "1",
            "data" : {
                "name" : "Бобик"
            }
        },
        "assert" : {
            "objectID.value" : "1"
        }
    }
    """
    И в networkID "1" создаем объект в структуре "dog"
    """
    {
        "request" : {
            "id" : "2",
            "data" : {
                "name" : "Тузик",
                "age" : 35,
                "weight" : 12.52
            }
        },
        "assert" : {
            "objectID.value" : "2"
        }
    }
    """



#FindByNetworkID
#ScenarioDirectoriesMapping
