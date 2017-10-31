Функционал: API base CRUD

Сценарий: выполняются предусловия для тестирования API
    Если есть кешированое значение cookie с именем sessionid
    Если указаны app_id и app_secret

@wip
Сценарий: создание тестовой структуры, добавление полей
    Допустим работает шаг "Если есть кешированое значение cookie с именем sessionid"
    И отправляем авторизованный запрос на "/good/api/v3/object/filters/"
    """
    {"sysName":"dog",
    "name":"dog","id":"0","parentID":"0","fastCreate":false,"fastCreatePayload":"","sourceSysName":"","action":"create"}
    """
    К тому же отправляем авторизованный запрос на "/good/api/v3/object/structure/"
    """
    {"filterName":"dog",
    "structure":[
      {"sysName":"id","name":"id","dataType":"id","id":"0","link":"","group":"","tags":"","indexing":false,"ordering":false,"linkIndexFieldSysName":[]},
      {"isEditMode":true,"isNew":true,"id":1509100441582,"sysName":"fieldName","name":"fieldName","dataType":"string","link":"","linkIndexFieldSysName":[""]}
    ]}
    """



@wip
Сценарий: сохранение объекта структуры и поиск его
    Допустим работает шаг "Если указаны app_id и app_secret"
    Если сохраняем объект структуры "dog"
    """
    {
        "id": "42",
        "fieldName": "Chubaka"
    }
    """
    То существует объект структуры "dog" с id "42"
    И объект структуры "dog" имеет поля
    """
    {
        "filter": 
            {"filters":[{"operator":"AND","field":"id","value":"42","exp":"=="}],"fetch":"","fields":"","pageSize":10,"page":0,"ref":"","allObjects":true,"orders":[]}
        ,
        "assert": {
            "id": "42",
            "fieldName": "Chubaka"
        }
    }
    """
