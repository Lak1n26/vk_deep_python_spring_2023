# Библиотека для парсинга и сериализации json (с помощью C API)

cjson.c: модуль cjson, который имеет два метода: loads и dumps для десериализации и сериализации JSON соответственно

setup.py: установка библиотеки cjson

main.py: тесты производительности (сравнение cjson с json и ujson)

tests_cjson.py: тесты корректности работы

Makefile: создается и активируется виртуальное окружение в папку venv с установкой всех необходимых библиотек;
          make test активирует виртуальное окружение и запускает tests_cjson.py.
