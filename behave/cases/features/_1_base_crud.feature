Функционал: _Этап 1 - API base CRUD

Сценарий: выполняются предусловия для тестирования API
    Если есть кешированое значение cookie с именем sessionid
    Если указаны app_id и app_secret


Сценарий: создание тестовой структуры, добавление полей в метаинформацию
    Допустим работает шаг "Если есть кешированое значение cookie с именем sessionid"
    И отправляем авторизованный запрос на "/good/api/v3/object/filters/"
    """
    {"sysName":"cat",
    "name":"cat","id":"0","parentID":"0","fastCreate":false,"fastCreatePayload":"","sourceSysName":"","action":"create"}
    """
    И отправляем авторизованный запрос на "/good/api/v3/object/filters/remove"
    """
    {
        "action":"remove",
        "sysName":"cat"
    }
    """
    К тому же отправляем авторизованный запрос на "/good/api/v3/object/structure/"
    """
    {"filterName":"cat",
    "structure":[
      {"sysName":"id","name":"id","dataType":"id","id":"0","link":"","group":"","tags":"","indexing":false,"ordering":false,"linkIndexFieldSysName":[]},
      {"isEditMode":true,"isNew":true,"id":1509100441582,"sysName":"catName","name":"catName","dataType":"string","link":"","linkIndexFieldSysName":[""]},
      {"isEditMode":true,"isNew":true,"id":1509100441582,"sysName":"catHeight","name":"catHeight","dataType":"number","link":"","linkIndexFieldSysName":[""]}
    ]}
    """


Сценарий: сохранение объекта структуры и его поиск
    Допустим работает шаг "Если указаны app_id и app_secret"
    Если сохраняем объект структуры "cat"
    """
    {
        "id": "42",
        "catName": "Chubaka"
    }
    """
    То существует объект структуры "cat" с id "42"
    И объект структуры "cat" имеет поля
    """
    {
        "filter": 
            {"filters":[{"operator":"AND","field":"id","value":"42","exp":"=="}],"fetch":"","fields":"","pageSize":10,"page":0,"ref":"","allObjects":true,"orders":[]}
        ,
        "assert": {
            "id": "42",
            "catName": "Chubaka"
        }
    }
    """
