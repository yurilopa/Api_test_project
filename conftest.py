import pytest
import requests
import allure
import os
import sys
# Добавляем текущую директорию в путь (где находится папка endpoints)
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
#from test_api_fin_project.
from endpoints.create_meme import (CreateMeme)
#from test_api_fin_project.
from endpoints.update_meme import (UpdateMeme)
#from test_api_fin_project.
from endpoints.get_meme import (GetMeme)
#from test_api_fin_project.
from endpoints.delete_meme import (DeleteMeme)


# Создаем экземпляр класса CreateMeme
@pytest.fixture()
def create_new_three_memes():
    return CreateMeme()

@pytest.fixture()  # инициализация create_post_endpoint() исп в test
def create_meme_endpoint():
    return CreateMeme()


@pytest.fixture()  # инициализация create_post_endpoint() исп в test
def get_meme_endpoint():
    return GetMeme()  # Подчеркивание GetObj означает, что Python не может найти этот класс из-за отсутствующего импорта


@pytest.fixture()  # инициализация create_post_endpoint() исп в testpy
def update_meme_endpoint():
    return UpdateMeme()


@pytest.fixture()  # инициализация create_post_endpoint() исп в test
def delete_meme_endpoint():
    return DeleteMeme()

"""Создает новый токен по имени отдаем его в тесты в папке test_dir"""
@pytest.fixture(scope="session")
@allure.feature('Posts')
@allure.story('Manipulate post')
def new_token():
    body = {"name": "Yuri Tester"}
    headers = {'Content-Type': 'application/json'}
    response = requests.post('http://memesapi.course.qa-practice.com/authorize', json=body, headers=headers)
    # Проверка успешности запроса
    assert response.status_code == 200, f"Failed to create token: {response.text}"
    token = response.json()['token']  # тут в token будет хранится ответ в виде token из json
    print(f'Created user with token: {token}')
    yield token
    print('test life token')  # Teardown - проверяем жизненный цикл токена
    check_response = requests.get(f'http://memesapi.course.qa-practice.com/authorize/{token}')
    if check_response.status_code == 200:
        print('Token still exists and valid')
    else:
        print(f'Token check failed with status: {check_response.status_code}')


"""Готовые заголовки с авторизацией"""
# @pytest.fixture()
# def auth_header():
#     return {'Content-Type': 'application/json', 'Autharization': new_token}


"""Создаем новый мем и отдаем его ID для тестов в папке test_dir"""
@pytest.fixture()
@allure.feature('Posts')
@allure.story('Manipulate post')
def new_meme_id(new_token):
    body = {
        'text': "Cat",
        'url': "https://images.chesscomfiles.com/uploads/v1/blog/640393.672c38ed.668x375o.1e02a635934e@2x.jpeg",
        'tags': ["meme m", "Cat"],
        'info': {"topic": ["cat", "loading"]}
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': new_token
    }
    # print('Создает новый мем')
    response = requests.post('http://memesapi.course.qa-practice.com/meme', json=body, headers=headers)
    # print(response)
    assert response.status_code == 200, f'Failed to create meme: {response.text}'
    # meme_data = response.json()
    meme_id = response.json()['id']  # тут в self.post_id будет хранить ответ в виде id из json
    print(f'Created meme with ID: {meme_id}')
    with allure.step(f'Check status code for test test_create_three_new_meme_id is: {response.status_code}'):
        assert response.status_code == 200
    meme_id = response.json()['id']  # тут в self.post_id будет хранить ответ в виде id из json
    print(f'Created meme with id: {meme_id}')
    yield meme_id
    print(f'Meme {meme_id} lifecycle finished')
    # print('deleting meme')
    # requests.delete(f'http://memesapi.course.qa-practice.com/meme/{meme_id}')

# Дополнительные полезные фикстуры
"""Тестовые данные пользователя"""
@pytest.fixture(scope="session")
def test_user_data():
    return {
        'name': 'Yuri tester',
        'text': 'Somthing very interesting text',
        'tags': ['memes', 'adult']
    }


"""Невалидный токен для негативных тестов"""
@pytest.fixture()
def invalid_token():
    return invalid_token('invalid0token09o1234321')


"""Стандартные данные для создания тестового мема"""
@pytest.fixture()
def test_meme_data():
    return {
        'text': 'Somthing interesting text',
        'url': 'https://img.championat.com/i/u/l/1745295935682006297.jpg',
        'tags': ['info', 'cats'],
        'info': {'test': True, 'framework': 'pytest'}
    }


@pytest.fixture()
@allure.feature('Example')
@allure.story('Equals')
def num():
    return 5
