import pytest
import requests
import allure
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
from endpoints.create_meme import (CreateMeme)
from endpoints.update_meme import (UpdateMeme)
from endpoints.get_meme import (GetMeme)
from endpoints.delete_meme import (DeleteMeme)
from endpoints.auth_calss import (GetToken)


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


@pytest.fixture()  # инициализация create_post_endpoint() исп в test
def create_token():
    return GetToken()


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
    response = requests.post('http://memesapi.course.qa-practice.com/meme', json=body, headers=headers)
    with allure.step(f'Check status code for test test_create_three_new_meme_id is: {response.status_code}'):
        assert response.status_code == 200
    meme_id = response.json()['id']  # тут в self.post_id будет хранить ответ в виде id из json
    print(f'Created meme with id: {meme_id}')
    yield meme_id
    print(f'Meme {meme_id} lifecycle finished')
    delete_endpoint = DeleteMeme()
    delete_endpoint.meme_id = meme_id
    delete_response = delete_endpoint.delete_meme(meme_id, headers)
    if delete_response.status_code == 200:
        print(f'Object {meme_id} successfully deleted')
    elif delete_response.status_code == 404:
        print(f'Object {meme_id} deleted in test')
    else:
        print(f'Unexpected status code deletion {delete_response.status_code}')


"""Тестовые данные пользователя"""
@pytest.fixture(scope="session")
def user_data():
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
def meme_data():
    return {
        'text': 'Somthing interesting text',
        'url': 'https://img.championat.com/i/u/l/1745295935682006297.jpg',
        'tags': ['info', 'cats'],
        'info': {'test': True, 'framework': 'pytest'}
    }
