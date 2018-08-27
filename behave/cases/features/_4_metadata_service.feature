Функционал: Работа с mongodb-service

#@wip
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
            "objectID.value" : "1",
            "networkID.value" : 1,
            "data.values.['name'].stringValue.value" : "Бобик"
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
            "objectID.value" : "2",
            "networkID.value" : 1,
            "data.values.['name'].stringValue.value" : "Тузик",
            "data.values.['age'].intValue.value" : 35,
            "data.values.['weight'].doubleValue.value" : 12.52
        }
    }
    """
    Тогда в networkID "1" существует объект в структуре "dog" с id="1"
    И в networkID "1" существует объект в структуре "dog" с id="2"
    Если в networkID "1" изменим поля в структуре "dog" с id="2"
    """
    {
        "request" : {
            "data" : {
                "name" : "Гектор"
            }
        },
        "assert" : {
            "value" : {
                "objectID.value" : "2",
                "networkID.value" : 1,
                "data.values.['name'].stringValue.value" : "Гектор"
            }
        }
    }
    """
    То в networkID "1" ищем по структуре "dog"
    """
    {
        "filters" : {
        },
        "assert" : {
            "value.values.[1]" : {
                "objectID.value" : "2",
                "networkID.value" : 1,
                "data.values.['name'].stringValue.value" : "Гектор",
                "data.values.['age'].intValue.value" : 35,
                "data.values.['weight'].doubleValue.value" : 12.52
            }
        }
    }
    """
    И в networkID "1" ищем по структуре "dog"
    """
    {
        "filters" : {
            "op" : "all",
            "innerFilters" : [
                {
                    "op" : "==",
                    "field" : "age",
                    "value" : "35"
                },
                {
                    "op" : "==",
                    "field" : "name",
                    "value" : "Гектор"
                }
            ]
        },
        "assert" : {
            "value.values.[0]" : {
                "objectID.value" : "2",
                "networkID.value" : 1,
                "data.values.['name'].stringValue.value" : "Гектор",
                "data.values.['age'].intValue.value" : 35,
                "data.values.['weight'].doubleValue.value" : 12.52
            }
        }
    }
    """
    Если в networkID "1" удаляем объект в структуре "dog" с id="1"
    То в networkID "1" ищем по структуре "dog"
    """
    {
        "filters" : {
            "op" : "==",
            "field" : "name",
            "value" : "Бобик"
        },
        "assert" : {
            "total" : 0
        }
    }
    """
    То в networkID "1" ищем по структуре "dog"
    """
    {
        "filters" : {
        },
        "assert" : {
            "total" : 1
        }
    }
    """




@wip
@metadata-service
@mongodb-service
Сценарий: Проверяем простые аггрегации, отчеты и поиск по индексу
    Допустим в networkID "1" удаляем структуру "users"
    И в networkID "1" удаляем структуру "city"
    И в networkID "1" создаем структуру "city" с полями
    """
    [
        {"sysName":"id","dataType":"id","name":"id","link":"","indexing":false,"ordering":false,"linkIndexFieldSysName":[],"arrayLink":false,"linkType":false,"linkOrArrayLinkType":false},
        {"sysName":"size","dataType":"string","name":"size","link":"","indexing":false,"ordering":false,"linkIndexFieldSysName":[],"arrayLink":false,"linkType":false,"linkOrArrayLinkType":false},
        {"sysName":"name","dataType":"string","name":"name","link":"","indexing":false,"ordering":false,"linkIndexFieldSysName":[],"arrayLink":false,"linkType":false,"linkOrArrayLinkType":false}
    ]
    """
    И в networkID "1" создаем структуру "users" с полями
    """
    [
        {"sysName":"id","dataType":"id","name":"id","link":"","indexing":false,"ordering":false,"linkIndexFieldSysName":[],"arrayLink":false,"linkType":false,"linkOrArrayLinkType":false},
        {"sysName":"name","dataType":"string","name":"name","link":"","indexing":false,"ordering":false,"linkIndexFieldSysName":[],"arrayLink":false,"linkType":false,"linkOrArrayLinkType":false},
        {"sysName":"age","dataType":"number","name":"age","link":"","indexing":false,"ordering":false,"linkIndexFieldSysName":[],"arrayLink":false,"linkType":false,"linkOrArrayLinkType":false},
        {"sysName":"city_id","dataType":"link","name":"city_id","link":"city","indexing":true,"ordering":false,"linkIndexFieldSysName":["size"],"arrayLink":false,"linkType":false,"linkOrArrayLinkType":true}
    ]
    """
    То в networkID "1" создаем множество объектов в структуре "city"
    """
    {
        "request" : [
            {
            "id" : "1",
            "data" : {
                "name" : "Москва",
                "size" : "XXL"
            }
            },
            {
                "id" : "2",
                "data" : {
                    "name" : "New York",
                    "size" : "XXL"
                }
            },
            {
                "id" : "3",
                "data" : {
                    "name" : "Самара",
                    "size" : "L"
                }
            },
            {
                "id" : "4",
                "data" : {
                    "name" : "Калуга",
                    "size" : "L"
                }
            }
        ]
    }
    """
    И в networkID "1" создаем множество объектов в структуре "users"
    """
    {
        "request" : [
            {
            "id" : "1",
            "data" : {
                "name" : "Петр",
                "age" : "33",
                "city_id" : "1"
            }
            },
            {
                "id" : "2",
                "data" : {
                    "name" : "Юрий",
                    "age" : "39",
                    "city_id" : "1"
                }
            },
            {
                "id" : "3",
                "data" : {
                    "name" : "Юлия",
                    "age" : "20",
                    "city_id" : "2"
                }
            },
            {
                "id" : "4",
                "data" : {
                    "name" : "Мария",
                    "age" : "28",
                    "city_id" : "2"
                }
            },
            {
                "id" : "5",
                "data" : {
                    "name" : "Григорий",
                    "age" : "45",
                    "city_id" : "3"
                }
            },
            {
                "id" : "6",
                "data" : {
                    "name" : "Федор",
                    "age" : "52",
                    "city_id" : "4"
                }
            }
        ]
    }
    """
    То в networkID "1" ищем по структуре "users"
    """
    {
        "filters" : {
            "op" : "all",
            "innerFilters" : [
                {
                    "op" : "==",
                    "field" : "city_id.size",
                    "value" : "L"
                }
            ]
        },
        "assert" : {
            "total" : 2
        }
    }
    """
    Если в networkID "1" строим аггрегацию по структуре "users"
    """
    {
        "request" : {
            "filters" : [],
            "aggregation" : "arrayField",
            "aggregationField" : "name"
        },
        "assert" : {
            "stringValue.value" : "Федор,Григорий,Петр,Мария,Юрий,Юлия"
        }
    }
    """

#FindByNetworkID
#ScenarioDirectoriesMapping

# List, TableSize, Report, ProcessObjects, ProcessObjectsWithFields, BatchFields, SimpleAggregate