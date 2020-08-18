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
4. В папке проекта создать файл с переменными окружения [.env](https://pypi.org/project/python-dotenv/):
   - Получить [SuperJob secret key](https://api.superjob.ru/register)
   - Создать в файле переменную с названием SJ_SECRET_KEY:
        ```sh
        SJ_SECRET_KEY=v3.r.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        ```

5. Запустить файл main.py
```sh
$ python3 path/main.py
```

## Цель проекта:
Проект написан в образовательных целях в рамках прохождения курса [API веб-сервисов](https://dvmn.org/modules/web-api)
платформы [DevMan](https://dvmn.org/)