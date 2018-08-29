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
                    "age" : 33,
                    "city_id" : "1"
                }
            },
            {
                "id" : "2",
                "data" : {
                    "name" : "Юрий",
                    "age" : 39,
                    "city_id" : "1"
                }
            },
            {
                "id" : "3",
                "data" : {
                    "name" : "Юлия",
                    "age" : 20,
                    "city_id" : "2"
                }
            },
            {
                "id" : "4",
                "data" : {
                    "name" : "Мария",
                    "age" : 28,
                    "city_id" : "2"
                }
            },
            {
                "id" : "5",
                "data" : {
                    "name" : "Григорий",
                    "age" : 45,
                    "city_id" : "3"
                }
            },
            {
                "id" : "6",
                "data" : {
                    "name" : "Федор",
                    "age" : 52,
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
    Если в networkID "1" строим аггрегацию по структуре "users"
    """
    {
        "request" : {
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
            "aggregation" : "arrayField",
            "aggregationField" : "name"
        },
        "assert" : {
            "stringValue.value" : "Федор,Григорий"
        }
    }
    """
    Если в networkID "1" создаем отчет по структуре "users"
    """
    {
        "request" : {
            "settings" : {
                "name" : "avg age and count / city size",
                "preFiltersType" : "AND",
                "postFiltersType" : "AND",
                "parameters" : [],
                "fields" : [
                    {
                        "field": "id",
                        "id": "id"
                    },
                    {
                        "field": "name",
                        "id": "name"
                    },
                    {
                        "field": "age",
                        "id": "age"
                    },
                    {
                        "field": "city_id",
                        "id": "city_id"
                    },
                    {
                        "field": "city_id.size",
                        "id": "city_id.size"
                    }
                ],
                "groups" : [{
                    "fields": [{
                        "field": "city_id.size",
                        "id": "city_id.size"
                    }],
                    "aggregations": [{
                        "field": "age",
                        "fn": "avg",
                        "id": "avg (age)",
                        "resultFieldName": ""
                    },{
                        "field": "id",
                        "fn": "count",
                        "id": "count (id)",
                        "resultFieldName": ""
                    }],
                    "id": "200"
                }],
                "preFilters" : [{
                    "exp": "!=",
                    "field": "name",
                    "value": "Петр",
                    "isExp": false
                }],
                "postFilters" : [{
                    "aggregationId": "count (id)",
                    "exp": ">",
                    "value": "2",
                    "isExp": true
                }]
            }
        },
        "assert" : {
            "filters" : {
            },
            "assert" : {
                "total": 1,
                "value.values.[0]" : {
                    "networkID.value" : 1,
                    "data.values.['id___count'].intValue.value" : 3,
                    "data.values.['city_id__size'].stringValue.value" : "XXL",
                    "data.values.['age___avg'].doubleValue.value" : 29.0
                }
            }
        }
    }
    """


@wip
@metadata-service
@mongodb-service
Сценарий: Проверяем потоковые методы
    Допустим в networkID "1" удаляем структуру "workers"
    И в networkID "1" создаем структуру "workers" с полями
    """
    [
        {"sysName":"id","dataType":"id","name":"id","link":"","indexing":false,"ordering":false,"linkIndexFieldSysName":[],"arrayLink":false,"linkType":false,"linkOrArrayLinkType":false},
        {"sysName":"name","dataType":"string","name":"name","link":"","indexing":false,"ordering":false,"linkIndexFieldSysName":[],"arrayLink":false,"linkType":false,"linkOrArrayLinkType":false},
        {"sysName":"age","dataType":"number","name":"age","link":"","indexing":false,"ordering":false,"linkIndexFieldSysName":[],"arrayLink":false,"linkType":false,"linkOrArrayLinkType":false}
    ]
    """
    То в networkID "1" генерируем "100" объектов в структуре "workers"
    """
    {
        "pattern" : {
            "id" : "%d",
            "data" : {
                "name" : "worker-%d"
            }
        }
    }
    """
    И в networkID "1" потоково собираем объекты из структуры "workers"
    """
    {
        "size" : 100
    }
    """
    И в networkID "1" потоково собираем поля "name" из структуры "workers"
    """
    {
        "size" : 100,
        "assert" : {
            "[0].values.values.['name'].stringValue.value" : "worker-0",
            "[99].values.values.['name'].stringValue.value" : "worker-99"
        }
    }
    """
    И в networkID "1" потоково собираем поля "unknown1, some2" из структуры "workers"
    """
    {
        "size" : 100,
        "assert" : {
            "[0].values.values.['unknown1'].stringValue.value" : null,
            "[99].values.values.['some2'].stringValue.value" : null,
            "[100]" : null
        }
    }
    """

#FindByNetworkID
#ScenarioDirectoriesMapping

# List, TableSize, ProcessObjects, ProcessObjectsWithFields, BatchFields