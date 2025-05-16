# API для проекта Yatube

## Описание

Данный проект представляет собой RESTful API для социальной сети блогеров Yatube. API позволяет пользователям публиковать посты, оставлять комментарии, подписываться на других авторов и организовывать посты по группам.

Проект решает задачу предоставления программного интерфейса для взаимодействия с данными социальной сети, что позволяет интегрировать Yatube с другими приложениями, создавать мобильные клиенты или использовать API для автоматизации различных задач.

**Основные возможности API:**

*   Аутентификация пользователей с использованием JWT-токенов.
*   CRUD-операции для постов (публикаций).
*   CRUD-операции для комментариев к постам.
*   Получение списка групп и информации о конкретной группе.
*   Управление подписками на авторов.
*   Пагинация для списков постов.
*   Поиск по подпискам.

## Технологии

*   Python 3.x
*   Django 3.x / 4.x
*   Django REST framework
*   Simple JWT (для аутентификации)
*   SQLite (база данных по умолчанию для разработки)
## Тестирование
Перед началом убедитесь что в консоли установлен PythonPath до Django проекта:
```
export PYTHONPATH=$HOME/path/to/project/api_final_yatube/yatube_api
```
Затем проводите тестирование
```
pytest -v
```
## Установка

Чтобы развернуть проект на локальной машине, следуйте этим шагам:

1.  **Клонируйте репозиторий:**
    ```bash
    git clone <URL_вашего_репозитория>
    cd <название_папки_проекта> # например, yatube_api_final
    ```

2.  **Создайте и активируйте виртуальное окружение:**
    ```bash
    python -m venv venv
    ```
    *   Для Linux/macOS:
        ```bash
        source venv/bin/activate
        ```
    *   Для Windows:
        ```bash
        venv\Scripts\activate
        ```

3.  **Установите зависимости:**
    Убедитесь, что у вас есть файл `requirements.txt` в корне проекта. Если его нет, вы можете создать его командой `pip freeze > requirements.txt` после установки всех необходимых пакетов.
    ```bash
    pip install -r requirements.txt
    ```
    Основные зависимости, которые должны быть в `requirements.txt`:
    ```
    django
    djangorestframework
    djangorestframework-simplejwt
    django-filter # Если используется для фильтрации
    # Pillow (для ImageField, если еще не установлен)
    # gunicorn (для развертывания на production, опционально для локальной разработки)
    ```

4.  **Примените миграции:**
    Находясь в директории проекта, где лежит `manage.py`:
    ```bash
    python manage.py migrate
    ```

5.  **Создайте суперпользователя (опционально, для доступа к админке):**
    ```bash
    python manage.py createsuperuser
    ```

6.  **(Опционально) Загрузите тестовые данные или создайте пользователей/группы:**
    Для корректной работы некоторых тестов (например, Postman-коллекции) или для ручного тестирования API может потребоваться создать пользователей (`regular_user`, `root`, `second_user`) и группы. Это можно сделать через админку (`/admin/`) или с помощью `manage.py shell`.

    Пример создания пользователя в `manage.py shell`:
    ```python
    from django.contrib.auth import get_user_model
    User = get_user_model()
    if not User.objects.filter(username='regular_user').exists():
        User.objects.create_user(username='regular_user', password='<ваш_пароль>')
    ```

7.  **Запустите сервер разработки:**
    ```bash
    python manage.py runserver
    ```
    По умолчанию API будет доступно по адресу `http://127.0.0.1:8000/api/v1/`.

## Документация API (Redoc)

После запуска сервера документация API, сгенерированная с помощью Redoc, будет доступна по адресу:
`http://127.0.0.1:8000/api/redoc/`

## Примеры запросов к API

Ниже приведены некоторые примеры запросов к API. Для запросов, требующих аутентификации, необходимо предварительно получить JWT-токен и передавать его в заголовке `Authorization: Bearer <your_access_token>`.

### 1. Получение JWT-токена

**Запрос:**
http
POST /api/v1/jwt/create/
Content-Type: application/json

{
    "username": "your_username",
    "password": "your_password"
}


Ответ (200 OK):

{
    "refresh": "eyJ0eX...",
    "access": "eyJ0eX..."
}


### 2. Получение списка всех публикаций

Запрос:

GET /api/v1/posts/



Или с пагинацией:

GET /api/v1/posts/?limit=5&offset=10



Ответ (200 OK, пример для запроса без пагинации):

[
    {
        "id": 1,
        "author": "username1",
        "text": "Текст первого поста.",
        "pub_date": "2023-10-27T10:00:00Z",
        "image": null,
        "group": 1
    },
    {
        "id": 2,
        "author": "username2",
        "text": "Текст второго поста.",
        "pub_date": "2023-10-27T11:00:00Z",
        "image": "http://127.0.0.1:8000/media/posts/image.jpg",
        "group": null
    }
]


### 3. Создание новой публикации (требуется аутентификация)

Запрос:

POST /api/v1/posts/
Authorization: Bearer <your_access_token>
Content-Type: application/json

{
    "text": "Мой новый замечательный пост!",
    "group": 1  // ID существующей группы (опционально)
}



Ответ (201 Created):

{
    "id": 3,
    "author": "current_user_username",
    "text": "Мой новый замечательный пост!",
    "pub_date": "2023-10-27T12:00:00Z",
    "image": null,
    "group": 1
}


### 4. Получение списка своих подписок (требуется аутентификация)

Запрос:

GET /api/v1/follow/
Authorization: Bearer <your_access_token>



Поиск по имени пользователя, на которого подписан:

GET /api/v1/follow/?search=author_username
Authorization: Bearer <your_access_token>



Ответ (200 OK):

[
    {
        "user": "current_user_username",
        "following": "author_username1"
    },
    {
        "user": "current_user_username",
        "following": "author_username2"
    }
]


### 5. Создание подписки (требуется аутентификация)

Запрос:

POST /api/v1/follow/
Authorization: Bearer <your_access_token>
Content-Type: application/json

{
    "following": "username_to_follow"
}



Ответ (201 Created):

{
    "user": "current_user_username",
    "following": "username_to_follow"
}
