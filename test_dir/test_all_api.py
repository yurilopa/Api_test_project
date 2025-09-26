import pytest
import allure
import sys
import os
# Добавляем путь к корню проекта
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from test_api_fin_project.endpoints.get_meme import (GetMeme)


@pytest.fixture(scope='session')
def start_testing():
    print('Start testing')
    yield
    print('Testing completed')

# =============================================================================
# GET TESTS
# =============================================================================
@allure.feature('Memes')
@allure.story('Get memes')
@allure.title('Получение всех мемов')
@pytest.mark.smoke
def test_get_all_memes(get_meme_endpoint, new_meme_id, new_token):
    print('Тест получения всех мемов')
    print(f'Using token: {new_token}')
    meme_id = new_meme_id
    headers = {'Authorization': new_token}
    get_meme_endpoint.get_meme(meme_id, headers)
    get_meme_endpoint.check_response_status_is_200()
    get_meme_endpoint.check_meme_id(new_meme_id)


"""Получаем существующий мем по ID который создан в файле conftest.py лежащий в папке, на папку выше"""
@allure.feature('Memes')
@allure.story('Get meme')
@allure.title('Получение одного мема')
@pytest.mark.smoke
def test_get_one_meme(get_meme_endpoint, new_meme_id, new_token):
    meme_id = new_meme_id
    print(f'Тест получения объекта по ID: {new_meme_id}')
    headers = {'Authorization': new_token}
    get_meme_endpoint.get_meme(meme_id, headers)
    get_meme_endpoint.check_response_status_is_200()
    get_meme_endpoint.check_meme_id(new_meme_id)


# =============================================================================
# GET NEGATIVE TESTS
# =============================================================================
"""Тест получения мема с несуществующим ID - должен вернуть 404"""
@allure.feature('Memes')
@allure.story('Get memes')
@allure.title('Обновление мема негативный тест')
@pytest.mark.medium
def test_get_meme_non_existent_id(get_meme_endpoint, new_token):
    fake_id = 99999
    with allure.step('Test GET with existent id'):
        print(f'Тест получения мема c несуществующим ID')
        headers = {'Authorization': new_token}

        # Получаем мем
        get_meme_endpoint.get_meme(fake_id, headers)

        # Проверки с allure шагами
        get_meme_endpoint.check_not_found_404()
        print(f'Non existent id test - Status: {get_meme_endpoint.response.status_code}')


"""Тест получения мема с неправильным токеном - должен вернуть 401"""
@allure.feature('Memes')
@allure.story('Get memes')
@allure.title('Обновление мема негативный тест')
@pytest.mark.medium
def test_get_meme_invalid_token(get_meme_endpoint, new_meme_id):
    meme_id = new_meme_id
    with allure.step('Test GET with invalid token'):
        print(f'Тест получения мема c неправильным токеном')
        bad_headers = {'Authorization': 'bad_token_123', 'Content-Type': 'application/json'}
        # Получаем мем
        get_one_meme = GetMeme()
        get_one_meme.get_meme(meme_id, bad_headers)

        # Проверки с allure шагами
        get_one_meme.check_bad_request_401()
        print(f'Invalid token status test - Status: {get_one_meme.response.status_code}')


"""Тест получения мема без токена - должен вернуть 401"""
@allure.feature('Memes')
@allure.story('Get memes')
@allure.title('GET запрос без токена авторизации')
@pytest.mark.medium
def test_get_meme_no_token(get_meme_endpoint, new_meme_id):
    meme_id = new_meme_id
    with allure.step('Test GET without authorization token'):
        print(f'Тест получения мема без token')
        no_auth_headers = {'Content-Type': 'application/json'}
        # Получаем мем
        get_meme_endpoint.get_meme(meme_id, no_auth_headers)

        # Проверки с allure шагами
        get_meme_endpoint.check_bad_request_401()
        print(f'No token status test - Status: {get_meme_endpoint.response.status_code}')


"""Тест получения мема с пустым токеном - может вернуть 400/401/500"""
@allure.feature('Memes')
@allure.story('Get memes')
@allure.title('GET запрос с пустым токеном авторизации')
@pytest.mark.medium
def test_get_meme_empty_token(get_meme_endpoint, new_meme_id):
    meme_id = new_meme_id
    with (allure.step('Test GET with empty token')):
        empty_auth_headers = {'Authorization': '', 'Content-Type': 'application/json'}
        # Получаем мем
        get_meme_endpoint.get_meme(meme_id, empty_auth_headers)

        # Проверки с allure шагами
        get_meme_endpoint.check_bad_request_401()
        print(f'No token status test - Status: {get_meme_endpoint.response.status_code}')

# =============================================================================
# PUT TESTS
# =============================================================================
"""Создает новых мемов с разными данными"""
@allure.feature('Memes')
@allure.story('Manipulate memes')
@allure.title('Создание трех мемов')
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
    body = {'text': text, 'url': url, 'tags': tags, 'info': info}
    headers = {'Authorization': new_token}
    meme_id = new_meme_id
    create_new_three_memes.create_new_meme(body=body, headers=headers)
    create_new_three_memes.check_response_status_is_200()
    create_new_three_memes.check_response_text(text, meme_id=meme_id)
    create_new_three_memes.check_response_url(url, meme_id=meme_id)
    create_new_three_memes.check_response_tags(tags, meme_id=meme_id)


"""Тест обновления мема (PUT) - базовый тест полного обновления"""
@allure.feature('Meme')
@allure.story('Manipulate meme')
@allure.title('Обновление мема (меняем все поля)')
@pytest.mark.medium
def test_put_basic_change_meme(update_meme_endpoint, new_meme_id, new_token):
    print('PUT запрос обновления всех полей мема')
    with allure.step('Test PUT basic test'):
        meme_id = new_meme_id
        headers = {'Authorization': new_token, 'Content-Type': 'application/json'}
        # Изменяем все поля в теле запроса
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
        update_meme_endpoint.check_response_status_is_200()
        update_meme_endpoint.check_response_text('o kak')
        update_meme_endpoint.check_response_url('https://opis-cdn.tinkoffjournal.ru/mercury/03-fav-memes-2025.jpg', meme_id)
        update_meme_endpoint.check_response_tags(["updated", "test", "automation"], meme_id)


"""Тест обновления только текстового поля через PUT"""
@allure.feature('Meme')
@allure.story('Manipulate meme')
@allure.title('Обновление объекта меняем текст в меме')
@pytest.mark.medium
def test_change_text_only_meme(update_meme_endpoint, new_meme_id, new_token):
    print('PUT запрос обновления поля текст в меме')
    with allure.step('Test PUT test change only text'):
        meme_id = new_meme_id
        print('Тест обновления текстового поля мема через (PUT)')
        headers = {'Authorization': new_token, 'Content-Type': 'application/json'}
        text = 'update text'
        # В теле запроса, меняем только текст
        body = {
            'id': new_meme_id,
            'text': text,
            'url': 'https://opis-cdn.tinkoffjournal.ru/mercury/03-fav-memes-2025.jpg',
            "tags": ["updated", "test", "automation"],
            "info": {"colors": ["black", "white"], 'updated': True},
            'updated_by': 'Yuri tester'
        }
        # Обновляем мем
        update_meme_endpoint.update_meme(meme_id, body, headers)
        # Проверки с allure шагами
        update_meme_endpoint.check_response_status_is_200()
        update_meme_endpoint.check_text_only_updated(text, meme_id)


"""Тест обновления URL через PUT"""
@allure.feature('Meme')
@allure.story('Manipulate meme')
@allure.title('Обновление объекта изменяем поле url')
@pytest.mark.medium
def test_change_url_only_meme(update_meme_endpoint, new_meme_id, new_token):
    print('PUT запрос обновления поля url в меме')
    with allure.step('Test PUT test change only url'):
        meme_id = new_meme_id
        print('Тест обновления поля url мема через (PUT)')
        headers = {'Authorization': new_token, 'Content-Type': 'application/json'}
        # В теле запроса изменяем только url
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
        update_meme_endpoint.check_response_status_is_200()
        update_meme_endpoint.check_url_only_updated(new_url, meme_id)


"""Тест обновления tags через PUT"""
@allure.feature('Meme')
@allure.story('Manipulate meme')
@allure.title('Обновление мема изменяем поле тэги')
@pytest.mark.medium
def test_change_tag_only_meme(update_meme_endpoint, new_meme_id, new_token):
    print('PUT запрос обновления поля теги в меме')
    with allure.step('Test PUT test change only tags'):
        meme_id = new_meme_id
        headers = {'Authorization': new_token, 'Content-Type': 'application/json'}
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
        update_meme_endpoint.check_response_status_is_200()
        update_meme_endpoint.check_tags_only_updated(new_tags, meme_id)


"""Тест обновления info через PUT"""
@allure.feature('Meme')
@allure.story('Manipulate meme')
@allure.title('Обновление мема изменяем поле инфо')
@pytest.mark.medium
def test_change_info_only_meme(update_meme_endpoint, new_meme_id, new_token):
    print('PUT запрос обновления поля инфо в меме')
    with allure.step('Test PUT test change only info'):
        meme_id = new_meme_id
        headers = {'Authorization': new_token, 'Content-Type': 'application/json'}
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
        update_meme_endpoint.check_response_status_is_200()
        update_meme_endpoint.check_info_only_updated(new_info, meme_id)


# =============================================================================
# PUT BOUNDARY TESTS
# =============================================================================
@pytest.mark.parametrize("text,test_name,expected_status", [
    ("Very long text " * 100, "long_text", 200),
    ("", "empty_text", 200),
    ("!@#$%^&*()_+=~|{[]}'?/><`", "special_chars", 200),
    ("Привет мир! 🚀", "unicode", 200),
    ("'; DROP TABLE memes; --", "sql_injection", 200)
])
@allure.feature('Memes')
@allure.story('Manipulate memes')
@pytest.mark.medium
def test_put_meme_check_text(update_meme_endpoint, new_meme_id, new_token, text, test_name, expected_status):
    print(f'PUT запрос с {test_name}')
    allure.dynamic.title(f'PUT запрос с {test_name}')
    with allure.step(f'Test PUT with {test_name}'):
        meme_id = new_meme_id
        headers = {'Authorization': new_token, 'Content-Type': 'application/json'}
        body = {
            'id': meme_id,
            'text': text,
            'url': 'https://opis-cdn.tinkoffjournal.ru/mercury/03-fav-memes-2025.jpg',
            "tags": ["test", "text", "boundary"],
            "info": {"text with spec text": len(text)},
            'updated_by': 'Tester'
        }
        # Обновляем мем
        update_meme_endpoint.update_meme(meme_id, body, headers)
        # Проверки с allure шагами
        update_meme_endpoint.check_response_status_is_200()
        update_meme_endpoint.check_test_text(text, test_name)
        print(f'Test PUT with spec text - Status: {update_meme_endpoint.response.status_code}')


"""Тест PUT запрос, в котором много тегов в тесте"""
@allure.feature('Memes')
@allure.story('Manipulate memes')
@allure.title('PUT запрос, в котором много тегов в тесте')
@pytest.mark.medium
def test_put_meme_many_tags(update_meme_endpoint, new_meme_id, new_token):
    print('PUT запрос, в котором много тегов в тесте')
    with allure.step('Test PUT with many_tags'):
        meme_id = new_meme_id
        headers = {'Authorization': new_token, 'Content-Type': 'application/json'}
        many_tags = [f"tag_{i}" for i in range(50)]  # 50 тегов
        body = {
            'id': meme_id,
            'text': 'Meme with many tags',
            'url': 'https://opis-cdn.tinkoffjournal.ru/mercury/03-fav-memes-2025.jpg',
            "tags": many_tags,
            "info": {"Meme with many tags": (many_tags)},
            'updated_by': 'Many Tags Tester'
        }
        # Обновляем мем
        update_meme_endpoint.update_meme(meme_id, body, headers)
        # Проверки с allure шагами
        update_meme_endpoint.check_response_status_is_200()
        update_meme_endpoint.check_test_with_many_tags(many_tags)
        print(f'Test PUT with many tags - Status: {update_meme_endpoint.response.status_code}')



"""Тест PUT запрос, в котором много инфо в тесте"""
@allure.feature('Memes')
@allure.story('Manipulate memes')
@allure.title('PUT запрос, в котором много инфо в тесте')
@pytest.mark.medium
def test_put_meme_many_info(update_meme_endpoint, new_meme_id, new_token):
    print('PUT запрос, в котором много инфо в тесте')
    with allure.step('Test PUT with many_info'):
        meme_id = new_meme_id
        headers = {'Authorization': new_token, 'Content-Type': 'application/json'}
        many_info = {f"key_{i}": f"value_{i}" * 50 for i in range(100)}  # 50 тегов
        body = {
            'id': meme_id,
            'text': 'Meme with many info',
            'url': 'https://opis-cdn.tinkoffjournal.ru/mercury/03-fav-memes-2025.jpg',
            "tags": ['many', 'info'],
            "info": many_info,
            'updated_by': 'Many Info Tester'
        }
        # Обновляем мем
        update_meme_endpoint.update_meme(meme_id, body, headers)
        # Проверки с allure шагами
        update_meme_endpoint.check_response_status_is_200()
        update_meme_endpoint.check_test_with_many_info(many_info)
        print(f'Test PUT with many_info - Status: {update_meme_endpoint.response.status_code}')


"""Тест PUT запрос, с неправильным Content-Type"""
@allure.feature('Memes')
@allure.story('Manipulate memes')
@allure.title('PUT запрос, с неправильным Content-Type')
@pytest.mark.medium
def test_put_meme_text_headers(update_meme_endpoint, new_meme_id, new_token):
    print('PUT запрос, с неправильным Content-Type')
    with allure.step('Test PUT with text Content-Type'):
        meme_id = new_meme_id
        headers = {'Authorization': new_token, 'Content-Type': 'text/plain'}
        body = {
            'id': meme_id,
            'text': "Wrong content type test",
            'url': 'https://opis-cdn.tinkoffjournal.ru/mercury/03-fav-memes-2025.jpg',
            "tags": ["wrong", "content-type"],
            "info": {"content_type": "text/plain"},
            'updated_by': 'Content-Type Tester'
        }
        # Обновляем мем
        update_meme_endpoint.update_meme(meme_id, body, headers)
        # Проверки с allure шагами
        update_meme_endpoint.check_bad_request_400()
        print(f'запрос, с Content-Type: text/plain - Status: {update_meme_endpoint.response.status_code}')


"""Тест PUT запрос, с неправильным Content-Type"""
@allure.feature('Memes')
@allure.story('Manipulate memes')
@allure.title('PUT запрос, с неправильным Content-Type')
@pytest.mark.medium
def test_put_meme_multipart_headers(update_meme_endpoint, new_meme_id, new_token):
    print('PUT запрос, с неправильным Content-Type')
    with allure.step('Test PUT with multipart/form-data Content-Type'):
        meme_id = new_meme_id
        headers = {'Authorization': new_token, 'Content-Type': 'multipart/form-data'}
        body = {
            'id': meme_id,
            'text': "multipart/form-data content type test",
            'url': 'https://opis-cdn.tinkoffjournal.ru/mercury/03-fav-memes-2025.jpg',
            "tags": ["multipart/form-data", "content-type"],
            "info": {"content_type": "multipart/form-data"},
            'updated_by': 'Content-Type Tester'
        }
        # Обновляем мем
        update_meme_endpoint.update_meme(meme_id, body, headers)
        # Проверки с allure шагами
        update_meme_endpoint.check_bad_request_400()
        print(f'запрос, с Content-Type: multipart/form-data - Status: {update_meme_endpoint.response.status_code}')


"""Тест PUT запрос, с пустыми обязательными полями"""
@allure.feature('Memes')
@allure.story('Manipulate memes')
@allure.title('PUT запрос, с пустыми обязательными полями')
@pytest.mark.medium
def test_put_meme_empty_body(update_meme_endpoint, new_meme_id, new_token):
    print('PUT запрос, с пустыми обязательными полями')
    with allure.step('Test PUT with empty required fields'):
        meme_id = new_meme_id
        headers = {'Authorization': new_token, 'Content-Type': 'application/json'}
        body = {
            'id': meme_id,
            'text': "",  # Пустой текст
            'url': "",  # Пустой URL
            "tags": [],  # Пустые теги
            "info": {},
            'updated_by': ''  # Пустое имя
        }
        # Обновляем мем
        update_meme_endpoint.update_meme(meme_id, body, headers)
        # Проверки с allure шагами. Может быть принято или отклонено - зависит от бизнес-логики
        update_meme_endpoint.check_response_status_is_200()
        update_meme_endpoint.check_test_with_empty_fields_body(body)
        print(f'Empty fields test - Status: {update_meme_endpoint.response.status_code}')


# =============================================================================
# PUT NEGATIVE TESTS - Разделены на отдельные тесты
# =============================================================================
"""Негативный тест - запрос с несуществующим ID"""
@allure.feature('Memes')
@allure.story('Manipulate memes')
@allure.title('PUT запрос с несуществующим ID')
@pytest.mark.medium
def test_put_meme_with_non_existent_id(update_meme_endpoint, new_meme_id, new_token, meme_data):
    print('PUT запрос с несуществующим ID')
    with allure.step('Test PUT with non-existent ID'):
        fake_id = 99999
        headers = {'Authorization': new_token, 'Content-Type': 'application/json'}
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
        # Проверки с allure шагами
        update_meme_endpoint.check_not_found_404()
        print(f'Non existent id test - Status: {update_meme_endpoint.response.status_code}')


"""Негативный тест с неправильным токеном"""
@allure.feature('Memes')
@allure.story('Manipulate memes')
@allure.title('PUT запрос с неправильным токеном')
@pytest.mark.medium
def test_put_meme_with_bad_token(update_meme_endpoint, new_meme_id, new_token, meme_data):
    print('PUT запрос с неправильным токеном')
    with allure.step('Test PUT with invalid token'):
        meme_id = new_meme_id
        headers = {'Authorization': 'bad_token_123', 'Content-Type': 'application/json'}
        body = {
            'id': meme_id,
            'text': "update with bad token 123",
            'url': 'https://opis-cdn.tinkoffjournal.ru/mercury/03-fav-memes-2025.jpg',
            "tags": ["updated with bad_token_123", "negative test"],
            "info": {"colors": ["black", "white"], 'updated': True},
            'updated_by': 'Bad token 123'
        }
        # Обновляем мем с неправильным токеном
        update_meme_endpoint.update_meme(new_meme_id, body, headers)
        # Проверки с allure шагами
        update_meme_endpoint.check_bad_request_401()
        print(f'Invalid token status test - Status: {update_meme_endpoint.response.status_code}')


"""Негативный тест с пустым токеном авторизации"""
@allure.feature('Memes')
@allure.story('Manipulate memes')
@allure.title('PUT запрос с пустым токеном авторизации')
@pytest.mark.medium
def test_put_meme_with_empty_token(update_meme_endpoint, new_meme_id, new_token, meme_data):
    print('PUT запрос с пустым токеном авторизации')
    with allure.step('Test PUT with empty token'):
        meme_id = new_meme_id
        empty_auth_headers = {'Authorization': '', 'Content-Type': 'application/json'}
        body = {
            'id': meme_id,
            'text': "update with empty token",
            'url': 'https://opis-cdn.tinkoffjournal.ru/mercury/03-fav-memes-2025.jpg',
            "tags": ["updated with empty token", "negative test"],
            "info": {"colors": ["black", "white"], 'updated': True},
            'updated_by': 'empty token'
        }
        update_meme_endpoint.update_meme(meme_id, body, empty_auth_headers)
        actual_status = update_meme_endpoint.response.status_code
        update_meme_endpoint.check_bad_request_401()
        print(f'Empty token test status code: {actual_status}')


"""Негативный тест без токена авторизации"""
@allure.feature('Memes')
@allure.story('Manipulate memes')
@allure.title('PUT запрос без токена')
@pytest.mark.medium
def test_put_meme_with_outh_token(update_meme_endpoint, new_meme_id, new_token, meme_data):
    print('PUT запрос без токена')
    with allure.step('Test PUT without authorization token'):
        meme_id = new_meme_id
        headers = {'Content-Type': 'application/json'}
        body = {
            'id': meme_id,
            'text': "update with no auth headers",
            'url': 'https://opis-cdn.tinkoffjournal.ru/mercury/03-fav-memes-2025.jpg',
            "tags": ["updated with bad_token_123", "negative test"],
            "info": {"colors": ["black", "white"], 'updated': True},
            'updated_by': 'Bad User'
        }
        # Обновляем мем с неправильным токеном
        update_meme_endpoint.update_meme(new_meme_id, body, headers)
        # Проверки с allure шагами
        update_meme_endpoint.check_bad_request_401()
        update_meme_endpoint.check_response_text('Unauthorized')
        print(f'Invalid token status test - Status: {update_meme_endpoint.response.status_code}')


"""Негативный тест с невалидным URL"""
@allure.feature('Memes')
@allure.story('Manipulate memes')
@allure.title('PUT запрос с невалидным URL')
@pytest.mark.medium
def test_put_meme_with_bad_url(update_meme_endpoint, new_meme_id, new_token, meme_data):
    print('PUT запрос с невалидным URL')
    with allure.step('Test PUT with invalid URL'):
        meme_id = new_meme_id
        headers = {'Authorization': new_token, 'Content-Type': 'application/json'}
        invalid_url_body = {
            'id': meme_id,
            'text': "Test with invalid URL",
            'url': 'invalid-url-format',  # Невалидный URL
            "tags": ["invalid", "url", "test"],
            "info": {"url_valid": False},
            'updated_by': 'URL Tester'
        }
        # Обновляем мем с неправильным токеном
        update_meme_endpoint.update_meme(new_meme_id, invalid_url_body, headers)
        # Проверки с allure шагами. Может вернуть 400 или принять запрос - зависит от валидации API
        update_meme_endpoint.check_response_status_is_200()
        print(f'Invalid URL test - Status: {update_meme_endpoint.response.status_code}')


"""Негативный тест без авторизации"""
@allure.feature('Memes')
@allure.story('Manipulate memes')
@allure.title('PUT запрос без авторизации')
@pytest.mark.medium
def test_put_meme_with_no_outh(update_meme_endpoint, new_meme_id, new_token, meme_data):
    # Тест PUT без авторизации - создаем отдельный мем для этого теста
    meme_id = new_meme_id
    print('Негативный тест PUT запрос без авторизации')
    with allure.step('Test PUT without authorization'):
        body = {
            'id': meme_id,
            'text': "meme for test unauthorized",
            'url': 'https://img.championat.com/i/q/v/1745262596102423087.jpg',
            "tags": ["non authorized", "un auth", "without authorized"],
            "info": {'authorized': False},
            'updated_by': 'anon tester'
        }
        # Обновляем мем no auth
        no_auth_headers = {'Content-Type': 'application/json'}
        update_meme_endpoint.update_meme(meme_id, body, no_auth_headers)
        # Проверяем статус код
        update_meme_endpoint.check_bad_request_401()
        print(f'Test no auth - Status: {update_meme_endpoint.response.status_code}')
