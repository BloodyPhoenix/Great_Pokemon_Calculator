# Великий покемонячий калькулятор

#### Версия 0.25 - alpha

Далее - ВПК

### Великий покемонячий кальукулятор - приложение, основная цель которого - предоставление информации ипомощь тренеру в организации его команды покемонов в различных играх, а также учёт его покемонов.

## Основной стек 
- Kivy, в том числе файлы с разрешением .kv, для создания Графиечского интерфейса 
- пользователя
- Postgresql в качестве платформы для хранения и обработки данных о покемонах и
- пользователях
- SQLAlchemy в качестве orm
- BS4 для автоматического обновления информации в базах с помощью внешних источников, 
например, скраппинга с сайта serebii.net


## Структура приложения

- Файл main.py - основной файл приложения, в котором происходит подгрузка всех 
необходимых переменных и файлов и запуск приложения
- databases - директория, в которой хранится всё, что связано с базами данных, включая
их структуру, скрапперы для их автоматического обновления и скрипты, ответственные 
за получение информации по какой-то конкретной игре.
- GUI - директория, в которой находится всё, что связно с графическим интерфейсом 
пользователя, включая файлы с расширением .kv
- utils - директория, в которой находится вся прочая информация, не связанная непосредственно
ни с базой, ни с интерфейсом. Также фильтры для получения информации из базы. Фильтры 
относятся к этой категории потому, что при их применении идёт работа с данными, до этого
уже полученными из базы.
- Особенностью структуры является то, что одни и те же шаблоны экранов могут 
использоваться для отображения разных наборов данных. Поэтому экраны и различные 
функции для получения данных связаны через систему словарей. Такие словари содержат в 
качестве пар "ключ-значение" название игры, для которой нужно получить какие-то данные,
и функцию, которая формирует запрос к базе и возвращает ответ. Поэтому большинство экранов
имеют атрибут game, который используется для дальнейшего уточнения, какие именно функции 
следует вызывать для получения данных, по каким шаблонам отражать подробную информацию
и т.д. Зачастую словари вынесены в служебные файлы __init__ тех модулей, в которых 
находятся перечисленные в них функции. 


## Функционал

### Текущий:
 - Просмотр и обновление в автоматическом режиме данных об игре Pokemon Go
 - Фильтрация покемонов по их типу, боевой силе, номеру. Поиск по названию.
 - Просмотр индивидуальной странички покемона, в том числе - спика его атак.


### Планируемый в версии 0.3:
- Регистрация новых пользователей. Назвачение пользователю права ручного редактирования 
данных о покемонах и их атаках.
- Создание возможности ручного редактирования данных в базах.

### Планируемый в версии 0.35:
- Возможность пользователю регистрировать собственных покемонов в базе. Просмотр 
своих покемонов, фильтрация, изменение информации о них.

### TBA:
- Обновление структуры фильтров для удоства поиска и подбора команды для разных форматов 
лиги Го. 
- Присовение покемонам статуса мифических/легендарных/мегаэволюций и обновление фильтров
в соответствии с новыми данными.
- Создание отображения эволюционной цепочки и требований к эволюции.
- Создание скраппера для получения информации о покемонах из других игр.