import pytest
import allure
import sys
import os
# Добавляем путь к корню проекта
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from test_api_fin_project.endpoints.create_meme import (CreateMeme)
from test_api_fin_project.endpoints.update_meme import (UpdateMeme)
from test_api_fin_project.endpoints.get_meme import (GetMeme)
from test_api_fin_project.endpoints.delete_meme import (DeleteMeme)


@pytest.fixture(scope='session')
def start_testing():
    print('Start testing')
    yield
    print('Testing completed')


@allure.feature('Posts')
@allure.story('Get post')
@allure.title('Получение всех объектов')
@pytest.mark.smoke
def test_get_all_memes(get_meme_endpoint, new_meme_id, new_token):
    print('Тест получения всех мемов')
    print(f'Using token: {new_token}')
    meme_id = new_meme_id
    headers = {'Authorization': new_token}
    get_one_meme = GetMeme()
    get_one_meme.get_meme(meme_id, headers)
    get_one_meme.check_status_code(200)


"""Получаем существующий мем по ID который создан в файле conftest.py лежащий в папке, на папку выше"""
@allure.feature('Posts')
@allure.story('Get post')
@allure.title('Получение одного поста')
@pytest.mark.smoke
def test_get_one_meme(get_meme_endpoint, new_meme_id, new_token):
    meme_id = new_meme_id
    print(f'Тест получения объекта по ID: {new_meme_id}')
    headers = {'Authorization': new_token}
    get_one_meme = GetMeme()
    get_one_meme.get_meme(meme_id, headers)
    get_one_meme.check_status_code(200)
    get_one_meme.check_meme_id(new_meme_id)


"""Создает новых объектов с разными данными"""


@allure.feature('Posts')
@allure.story('Manipulate post')
@allure.title('Создание трех объектов')
@pytest.mark.parametrize('text, url, tags, info', [
    ("Corona Lisa",
     "https://i.pinimg.com/736x/96/56/33/965633b2d39204eda3ea3d110950c75e.jpg",
     ["meme", "Monaliza"],
     {"topic": ["art", "covid", "Mona Liza"]}
     ),
    ("Vinnie pooh",
     'https://img.rl0.ru/afisha/400x-/daily.afisha.ru/uploads/images/e/c3/ec32884e7a764498ab751454e812012a.jpg',
     ["mem", "Vinnie pooh"],
     {"topic": ["cartoon", "adult", "Vinnie pooh"]}
     ),
    ("Rofl",
     'https://www.anekdot.ru/i/caricatures/normal/25/8/4/1754318379.jpg',
     ["me", "Rofl"],
     {"topic": ["rofl", "cop", "scient"]}
     )
    ])
def test_create_three_new_meme(create_new_three_memes, text, url, tags, info, new_token, new_meme_id):
    create_meme_endpoint = CreateMeme()
    body = {'text': text, 'url': url, 'tags': tags, 'info': info}
    headers = {'Authorization': new_token}
    meme_id = new_meme_id
    create_meme_endpoint.create_new_meme(body=body, headers=headers)
    create_meme_endpoint.check_status_code(200)
    create_meme_endpoint.check_response_text(text, meme_id=meme_id)
    create_meme_endpoint.check_response_url(url, meme_id=meme_id)
    create_meme_endpoint.check_response_tags(tags, meme_id=meme_id)
    # requests.delete(f'http://memesapi.course.qa-practice.com/meme/{meme_id}')
    # print(f'Удаление объекта с id: {meme_id}')


"""Тест обновления объекта (PUT) - базовый тест полного обновления"""
@allure.feature('Posts')
@allure.story('Manipulate post')
@allure.title('Обновление объекта (меняем все поля)')
@pytest.mark.medium
def test_put_basic_change_meme(update_meme_endpoint, new_meme_id, new_token):
    # Создаем экземпляр класса
    update_meme_endpoint = UpdateMeme()
    meme_id = new_meme_id
    print('Тест обновления мема (PUT)')
    headers = {'Authorization': new_token, 'Content-Type': 'application/json'}
    # Получаем существующий мем
    existing_meme = update_meme_endpoint.getting_existing_meme(meme_id, headers)
    # В данные для обновления, берем оригинальную структуру и меняем нужные поля
    body = {
        'id': new_meme_id,
        'text': "o kak",
        'url': 'https://opis-cdn.tinkoffjournal.ru/mercury/03-fav-memes-2025.jpg',
        "tags": ["updated", "test", "automation"],
        "info": {"colors": ["black", "white"], 'updated': True},
        'updated_by': 'Yuri tester'
    }
    # Обновляем мем
    update_meme_endpoint.update_meme(meme_id, body, headers)
    # Все проверки с allure шагами
    update_meme_endpoint.check_status_code(200)
    update_meme_endpoint.check_response_text('o kak')
    update_meme_endpoint.check_response_url('https://opis-cdn.tinkoffjournal.ru/mercury/03-fav-memes-2025.jpg', meme_id)
    update_meme_endpoint.check_response_tags(["updated", "test", "automation"], meme_id)
    #update_meme_endpoint.check_response_info({"colors": ["black", "white"], "updated": True}, meme_id)

"""Тест обновления только текстового поля через PUT"""
@allure.feature('Posts')
@allure.story('Manipulate post')
@allure.title('Обновление объекта меняем текст в мема')
@pytest.mark.medium
def test_change_text_only_meme(update_meme_endpoint, new_meme_id, new_token):
    # Создаем экземпляр класса
    update_meme_endpoint = UpdateMeme()
    meme_id = new_meme_id
    print('Тест обновления текстового поля мема через (PUT)')
    headers = {'Authorization': new_token, 'Content-Type': 'application/json'}
    #Получаем существующий мем
    existing_meme = update_meme_endpoint.getting_existing_meme(meme_id, headers)
    print(f'Original meme {existing_meme}')
    # В данных для обновления, меняем только текст
    body = {
        'id': new_meme_id,
        'text': "update text",
        'url': 'https://opis-cdn.tinkoffjournal.ru/mercury/03-fav-memes-2025.jpg',
        "tags": ["updated", "test", "automation"],
        "info": {"colors": ["black", "white"], 'updated': True},
        'updated_by': 'Yuri tester'
    }

    # Обновляем мем
    update_meme_endpoint.update_meme(meme_id, body, headers)

    # Проверки с allure шагами
    update_meme_endpoint.check_status_code(200)
    update_meme_endpoint.check_text_only_updated('update text', meme_id)


"""Тест обновления URL через PUT"""
@allure.feature('Posts')
@allure.story('Manipulate post')
@allure.title('Обновление объекта изменяем поле url')
@pytest.mark.medium
def test_change_url_only_meme(update_meme_endpoint, new_meme_id, new_token):
    # Создаем экземпляр класса
    update_meme_endpoint = UpdateMeme()
    meme_id = new_meme_id
    print('Тест обновления поля url мема через (PUT)')
    headers = {'Authorization': new_token, 'Content-Type': 'application/json'}
    # Получаем существующий мем
    existing_meme = update_meme_endpoint.getting_existing_meme(meme_id, headers)
    print(f'Original meme {existing_meme}')
    # Берем оригинальную структуру и меняем d данных только url
    new_url = 'https://img.championat.com/i/f/f/17452621031297116737.jpg'
    body = {
        'id': new_meme_id,
        'text': "Meme with new image",
        'url': new_url,
        "tags": ["updated", "test", "automation"],
        "info": {"format": ["link", "txt"], 'image_changed': True},
        'updated_by': 'Yuri tester'
    }
    # Обновляем мем
    update_meme_endpoint.update_meme(meme_id, body, headers)

    # Проверки с allure шагами
    update_meme_endpoint.check_status_code(200)
    update_meme_endpoint.check_url_only_updated(new_url, meme_id)


"""Тест обновления tags через PUT"""
@allure.feature('Posts')
@allure.story('Manipulate post')
@allure.title('Обновление объекта изменяем поле тэги')
@pytest.mark.medium
def test_change_tag_only_meme(update_meme_endpoint, new_meme_id, new_token):
    # Создаем экземпляр класса
    update_meme_endpoint = UpdateMeme()
    meme_id = new_meme_id
    print('Тест обновления поля tags мема через (PUT)')
    headers = {'Authorization': new_token, 'Content-Type': 'application/json'}
    # Получаем существующий мем
    existing_meme = update_meme_endpoint.getting_existing_meme(meme_id, headers)
    print(f'Original meme {existing_meme}')
    # В данных для обновления, меняем только tags
    new_tags = ['update', 'tests']
    body = {
        'id': new_meme_id,
        'text': "Meme with new tags",
        'url': 'https://opis-cdn.tinkoffjournal.ru/mercury/03-fav-memes-2025.jpg',
        "tags": new_tags,
        "info": {"format": ["link", "txt"], 'tags changed': True},
        'updated_by': 'Yuri tester'
    }
    # Обновляем мем
    update_meme_endpoint.update_meme(meme_id, body, headers)

    # Проверки с allure шагами
    update_meme_endpoint.check_status_code(200)
    update_meme_endpoint.check_tags_only_updated(new_tags, meme_id)


"""Тест обновления info через PUT"""
@allure.feature('Posts')
@allure.story('Manipulate post')
@allure.title('Обновление объекта изменяем поле инфо')
@pytest.mark.medium
def test_change_info_only_meme(update_meme_endpoint, new_meme_id, new_token):
    # Создаем экземпляр класса
    update_meme_endpoint = UpdateMeme()
    meme_id = new_meme_id
    print('Тест обновления поля tags мема через (PUT)')
    headers = {'Authorization': new_token, 'Content-Type': 'application/json'}
    # Получаем существующий мем
    existing_meme = update_meme_endpoint.getting_existing_meme(meme_id, headers)
    print(f'Original meme {existing_meme}')
    # Берем оригинальную структуру и меняем только поле info
    new_info = {"colors": ["white", "grey"],
                    'rating': 9.5,
                    'viral': True,
                    'metadata': {'create data': 2019-10-16, 'author': 'Котизм'}
                    }
    body = {
        'id': new_meme_id,
        'text': "Meme with new info",
        'url': 'https://opis-cdn.tinkoffjournal.ru/mercury/03-fav-memes-2025.jpg',
        "tags": ["updated", "test", "automation"],
        "info": new_info,
        'updated_by': 'Yuri tester'
    }
    # Обновляем мем
    update_meme_endpoint.update_meme(meme_id, body, headers)

    # Проверки с allure шагами
    update_meme_endpoint.check_status_code(200)
    update_meme_endpoint.check_info_only_updated(new_info, meme_id)


"""Тесты граничных значений для PUT запросов"""
@allure.feature('Posts')
@allure.story('Manipulate post')
@allure.title('Тест граничных значений')
@pytest.mark.medium
def test_put_meme_boundary_values(update_meme_endpoint, new_meme_id, new_token):
    # Создаем экземпляр класса
    update_meme_endpoint = UpdateMeme()
    meme_id = new_meme_id
    print('Тесты граничных значений PUT')
    headers = {'Authorization': new_token, 'Content-Type': 'application/json'}

    # Тест 1: Очень длинный текст
    long_text = "Very long text " * 100  # Очень длинный текст
    body1 = {
        'id': new_meme_id,
        'text': long_text,
        'url': 'https://opis-cdn.tinkoffjournal.ru/mercury/03-fav-memes-2025.jpg',
        "tags": ["long", "text", "boundary"],
        "info": {"text_length": len(long_text)},
        'updated_by': 'Long Text Tester'
    }
    # Обновляем мем
    update_meme_endpoint.update_meme(meme_id, body1, headers)

    # Проверки с allure шагами
    update_meme_endpoint.check_boundary_status([200, 400])
    update_meme_endpoint.check_long_text(long_text)

    # Тест 2: Пустой текст
    empty_text = ""  # Пустой текст
    body2 = {
        'id': new_meme_id,
        'text': empty_text,
        'url': 'https://opis-cdn.tinkoffjournal.ru/mercury/03-fav-memes-2025.jpg',
        "tags": ["empty", "text", "boundary"],
        "info": {"empty text": (empty_text)},
        'updated_by': 'Empty Text Tester'
    }
    # Обновляем мем
    update_meme_endpoint.update_meme(meme_id, body2, headers)

    # Проверки с allure шагами
    update_meme_endpoint.check_boundary_status([200, 400])
    update_meme_endpoint.check_empty_text(empty_text)

    # Тест 3: Спец символы в тексте
    spec_text = "!@#$%^&*()_+=~|{[]}'?/><`"  # текст с спец символами
    body3 = {
        'id': new_meme_id,
        'text': spec_text,
        'url': 'https://opis-cdn.tinkoffjournal.ru/mercury/03-fav-memes-2025.jpg',
        "tags": ["spec", "text", "boundary"],
        "info": {"text with spec text": (spec_text)},
        'updated_by': 'Spec Text Tester'
    }
    # Обновляем мем
    update_meme_endpoint.update_meme(meme_id, body3, headers)

    # Проверки с allure шагами
    update_meme_endpoint.check_boundary_status([200, 400])
    update_meme_endpoint.check_text_with_spec_charts(spec_text)

    # Тест 4: много тегов в тесте
    many_tags = [f"tag_{i}" for i in range(50)]  # 50 тегов
    body4 = {
        'id': new_meme_id,
        'text': 'Meme with many tags',
        'url': 'https://opis-cdn.tinkoffjournal.ru/mercury/03-fav-memes-2025.jpg',
        "tags": many_tags,
        "info": {"Meme with many tags": (many_tags)},
        'updated_by': 'Many Tags Tester'
    }
    # Обновляем мем
    update_meme_endpoint.update_meme(meme_id, body4, headers)

    # Проверки с allure шагами
    update_meme_endpoint.check_boundary_status([200, 400])
    update_meme_endpoint.check_test_with_many_tags(many_tags)

    #Тест 5: много инфо в тесте
    many_info = {f"key_{i}": f"value_{i}" * 50 for i in range(100)}  # 50 тегов
    body5 = {
        'id': new_meme_id,
        'text': 'Meme with many info',
        'url': 'https://opis-cdn.tinkoffjournal.ru/mercury/03-fav-memes-2025.jpg',
        "tags": ['many', 'info'],
        "info": many_info,
        'updated_by': 'Many Info Tester'
    }
    # Обновляем мем
    update_meme_endpoint.update_meme(meme_id, body5, headers)

    # Проверки с allure шагами
    update_meme_endpoint.check_boundary_status([200, 400])
    update_meme_endpoint.check_test_with_many_info(many_info)

    # Тест 6: PUT с неправильным Content-Type
    with allure.step('Test PUT with wrong Content-Type'):
        wrong_headers = {'Authorization': new_token, 'Content-Type': 'text/plain'}
        simple_body = {
            'id': new_meme_id,
            'text': "Wrong content type test",
            'url': 'https://opis-cdn.tinkoffjournal.ru/mercury/03-fav-memes-2025.jpg',
            "tags": ["wrong", "content-type"],
            "info": {"content_type": "text/plain"},
            'updated_by': 'Content-Type Tester'
        }

        update_meme_endpoint.update_meme(new_meme_id, simple_body, wrong_headers)
        # Может вернуть 400, 415 (Unsupported Media Type) или принять
        update_meme_endpoint.check_status_code(500)
        print(f'Wrong Content-Type test - Status: {update_meme_endpoint.response.status_code}')

    # Тест 7: PUT с пустыми обязательными полями
    with allure.step('Test PUT with empty required fields'):
        empty_fields_body = {
            'id': new_meme_id,
            'text': "",  # Пустой текст
            'url': "",  # Пустой URL
            "tags": [],  # Пустые теги
            "info": {},
            'updated_by': ''  # Пустое имя
        }

        update_meme_endpoint.update_meme(new_meme_id, empty_fields_body, headers)
        # Может быть принято или отклонено - зависит от бизнес-логики
        update_meme_endpoint.check_boundary_status([200, 400])
        update_meme_endpoint.check_test_with_empty_fields_body(empty_fields_body)
        print(f'Empty fields test - Status: {update_meme_endpoint.response.status_code}')

"""Тест обновления объекта (PUT) - негативный тест обновления"""
@allure.feature('Posts')
@allure.story('Manipulate post')
@allure.title('Обновление объекта негативный тест')
@pytest.mark.medium
def test_put_meme_negative_cases(update_meme_endpoint, new_meme_id, new_token, test_meme_data):
    # Создаем экземпляры классов эндпоинта
    update_meme_endpoint = UpdateMeme()
    get_meme_endpoint = GetMeme()
    create_meme_endpoint = CreateMeme()
    #delete_meme_endpoint = DeleteMeme()
    #meme_id = new_meme_id
    print('Негативный тест обновления мема (PUT)')
    headers = {'Authorization': new_token, 'Content-Type': 'application/json'}
    #Получаем существующий мем
    with allure.step('Get existing mem for reference'):
        get_meme_endpoint.get_meme(new_meme_id, headers)
        get_meme_endpoint.check_status_code(200)
        print(f'Could got get mem: {get_meme_endpoint.response.status_code}')
        existing_meme = get_meme_endpoint.json
        print(f'Original meme {existing_meme}')

    # Тест 1: PUT с несуществующим ID
    with allure.step('Test PUT with non-existent ID'):
        fake_id = 99999
        body = {
            'id': fake_id,
            'text': "o kak",
            'url': 'https://opis-cdn.tinkoffjournal.ru/mercury/03-fav-memes-2025.jpg',
            "tags": ["updated", "test", "automation"],
            "info": {"colors": ["black", "white"], 'updated': True},
            'updated_by': 'Yuri tester'
        }
        # Обновляем мем с не существующим id
        update_meme_endpoint.update_meme(fake_id, body, headers)

        # Проверка статус кода
        update_meme_endpoint.check_status_code(404)
        #update_meme_endpoint.check_response_text('Not found')
        print(f'Non existent id test - Status: {update_meme_endpoint.response.status_code}')

    # Тест 2: PUT с неправильным токеном
    with allure.step('Test PUT with invalid token'):
        bad_headers = {'Authorization': 'bad_token_123', 'Content-Type': 'application/json'}
        body = {
            'id': new_meme_id,
            'text': "update with bad_token_123",
            'url': 'https://opis-cdn.tinkoffjournal.ru/mercury/03-fav-memes-2025.jpg',
            "tags": ["updated with bad_token_123", "negative test"],
            "info": {"colors": ["black", "white"], 'updated': True},
            'updated_by': 'Bad User'
        }
        # Обновляем мем с не существующим token
        update_meme_endpoint.update_meme(new_meme_id, body, bad_headers)

        # Проверка статус кода
        update_meme_endpoint.check_status_code(401)
        update_meme_endpoint.check_response_text('Unauthorized')
        print(f'Invalid token status test - Status: {update_meme_endpoint.response.status_code}')

    # Тест 2.1: PUT без токена авторизации
    with allure.step('Test PUT without authorization token'):
        no_auth_headers = {'Content-Type': 'application/json'}
        update_meme_endpoint.update_meme(new_meme_id, body, no_auth_headers)
        update_meme_endpoint.check_status_code(401)
        print('No token test passed')

    # Тест 2.2: PUT с пустым токеном
    with allure.step('Test PUT with empty token'):
        empty_auth_headers = {'Authorization': '', 'Content-Type': 'application/json'}
        # Обновляем мем с не существующим token
        print('Testing with empty authorization token')
        update_meme_endpoint.update_meme(new_meme_id, body, empty_auth_headers)
        actual_status = update_meme_endpoint.response.status_code
        print(f'Empty token test status code: {actual_status}')
        print(f'Response preview: {update_meme_endpoint.response.text[:100]}...')

        if actual_status == 500:
            # Сервер возвращает 500 для пустого токена
            update_meme_endpoint.check_status_code(500)
            print('Server returns 500 for empty token (potential server bug)')
        elif actual_status == 401:
            # Правильное поведение
            update_meme_endpoint.check_status_code(401)
            print('Empty token return correct status code')
        elif actual_status == 400:
            # Тоже допустимо - Bad Request
            update_meme_endpoint.check_status_code(400)
            print('Empty token returns 400 Bad Request')
        else:
            print(f'Unexpected status code for empty token: {actual_status}')
        # Принимаем любой ошибочный код как валидный для этого теста
        assert actual_status >= 400, f"Empty token should result in error, got {actual_status}"

    # Тест 4: PUT без авторизации - создаем отдельный мем для этого теста
    with allure.step('Test separate meme PUT request without authorization'):
        # Создаем отдельный мем для теста без авторизации
        create_body = {
            'text': "meme for test non authorization",
            'url': 'https://img.championat.com/i/q/v/1745262596102423087.jpg',
            "tags": ["non authorization", "unauthorized", "without authorization"],
            "info": {'authorization': False}
        }
        # Создаем тестовый мем
        create_meme_endpoint.create_new_meme(create_body, headers)
        create_meme_endpoint.check_status_code(200)
        test_meme_data = create_meme_endpoint.response.json()
        test_meme_id = test_meme_data['id']
        print(f'Create test meme with id: {test_meme_id}')

    with allure.step('Test PUT without authorization'):
        body = {
            'id': test_meme_id,
            'text': "meme for test unauthorized",
            'url': 'https://img.championat.com/i/q/v/1745262596102423087.jpg',
            "tags": ["non authorized", "un auth", "without authorized"],
            "info": {'authorized': False},
            'updated_by': 'anon tester'
        }
        # Обновляем мем no auth
        no_auth_headers = {'Content-Type': 'application/json'}
        update_meme_endpoint.update_meme(test_meme_id, body, no_auth_headers)
        # Проверяем статус код
        update_meme_endpoint.check_status_code(401)
        print(f'Test no auth - Status: {update_meme_endpoint.response.status_code}')

    # Тест 5: PUT с невалидным URL
    with allure.step('Test PUT with invalid URL'):
        invalid_url_body = {
            'id': new_meme_id,
            'text': "Test with invalid URL",
            'url': 'invalid-url-format',  # Невалидный URL
            "tags": ["invalid", "url", "test"],
            "info": {"url_valid": False},
            'updated_by': 'URL Tester'
        }

        update_meme_endpoint.update_meme(new_meme_id, invalid_url_body, headers)
        # Может вернуть 400 или принять запрос - зависит от валидации API
        update_meme_endpoint.check_negative_status
        print(f'Invalid URL test - Status: {update_meme_endpoint.response.status_code}')

        # Очистка: удаляем тестовый мем
    with allure.step('Clean up: Delete test meme'):
        delete_meme = DeleteMeme()
        delete_meme.delete_meme(test_meme_id, headers)
        delete_meme.check_status_code(200)
        print(f'Test meme {test_meme_id} deleted - Status: {delete_meme.response.status_code}')
