#Сравниваем вакансии программистов

Утилита, позволяющая проанализировать колличество вакансий по 10 языкам программирования, согласно рейтингу [GitHub](https://habr.com/ru/post/310262/)
, опубликованных за последний месяц, а так же средненюю зарплату по ним
согласно ресурсам:
 * [HeadHunter](https://hh.ru/)
 * [SuperJob](https://www.superjob.ru/)
 

 (Статистика получена из вакансий работодателей, которые указади верхние и нижние пороги заработной платы.)
 
## Как установить?
1. Уставновить Python 3+
```sh
$ sudo apt-get install python3
```
2. Установить, создать и активировать виртуальное окружение (Linux or MacOS)
```sh
$ pip install virtualenv
$ virtualenv vacancies_analyze
$ source vacancies_analyze/bin/activate
```
3. Установить файл с зависимостями
```sh
$ pip install -r requirements.txt
```

4. Запустить файл main.py
```sh
$ python3 run path/manage.py
```

## Цель проекта:
Проект написан в образовательных целях в рамках прохождения курса [API веб-сервисов](https://dvmn.org/modules/web-api)
платформы [DevMan](https://dvmn.org/)