#Feature: Licence keys
Функционал: _Этап 0 - Лицензионные ключи и вход в систему

#Scenario: Invalid licence key should show error message on activation
#    Given directual page /dashboard/login
#    And IF we on enter licence page
#    When we submit licence invalid_key as a key for user test_user@directual.com
#    Then system show us error message



#
#Scenario: Valid licence key should activate system
#    Given directual page /dashboard/login
#    And IF we on enter licence page
    #When we submit licence QEM76LDljaZhkTA0040itSdMqq4J2atX7GZSVNP3EpymLRUOvRQItcjgMI7shzYbMLJGgYMC7eTKTLD0WqebCifYWhuiyx0BkXNGaqnTUw3KMFaFe4nsdiznGxyp1xi0itPZOamO/6zVtjurfSKJS35t7WHF9cACSLkzU4+mvmA= as a key for user mts
#    Then system show us login page

#---------------


@minor
Сценарий: Ввод плохого ключа должен выводить ошибку
    Допустим открыли мы страницу платформы /
    И ждем 1.0 сек
    И это оказалась страница ввода лицензии
    Если мы вводим invalid_key в качестве ключа для пользователя test_user@directual.com
    То отображается ошибка

@critical
Сценарий: Ввод хорошего ключа должен активировать систему
    Допустим открыли мы страницу платформы /dashboard/login
    И это оказалась страница ввода лицензии
    Если мы вводим QEM76LDljaZhkTA0040itSdMqq4J2atX7GZSVNP3EpymLRUOvRQItcjgMI7shzYbMLJGgYMC7eTKTLD0WqebCifYWhuiyx0BkXNGaqnTUw3KMFaFe4nsdiznGxyp1xi0itPZOamO/6zVtjurfSKJS35t7WHF9cACSLkzU4+mvmA= в качестве ключа для пользователя mts
    То отображается страница входа


@blocker
#@wip
Сценарий: Вход в систему должен работать корректно
    Допустим открыли мы страницу платформы /dashboard/login
    И это оказалась страница входа в систему
    Если мы пытаемся ввойти в систему под логином admin и паролем 123456
    И обновляем страницу
    То установлена cookie с именем sessionid
    И отображается страница по пути /dashboard/cabinet
    К тому же сохраним значение cookie sessionid в кеш

