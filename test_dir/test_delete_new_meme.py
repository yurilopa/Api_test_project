import allure
import pytest
from test_api_fin_project.endpoints.delete_meme import (DeleteMeme)
from test_api_fin_project.endpoints.get_meme import (GetMeme)


"""
    Тест проверяет:
    1. Удаление выполняется успешно (200 OK)
    2. Мема больше нет в системе после удаления (404 Not Found)
"""
@allure.feature('Memes')
@allure.story('Manipulate meme')
@allure.title('Удаление мема')
def test_delete(delete_meme_endpoint, new_meme_id, new_token):
    meme_id = new_meme_id
    print(f'Тест удаления объекта: {meme_id}')
    headers = {'Authorization': new_token}
    # Шаг 1 удаление
    delete_meme = DeleteMeme()
    delete_meme.delete_meme(meme_id, headers)
    delete_meme.check_response_status_is_200()
    # Шаг 2: ПРОВЕРЯЕМ что удалён
    get_meme_check = GetMeme()
    get_meme_check.get_meme(meme_id, headers)
    get_meme_check.check_not_found_404()
    print(f'✓ Мем {meme_id} не найден - удаление подтверждено')


"""
    Тест проверяет:
    1. Удаление выполняется успешно (200 OK)
    2. Мема больше нет в системе после удаления (404 Not Found)
    3. Попытка повторного удаления уже удаленного на 2 шаге мема
"""
@allure.feature('Memes')
@allure.story('Manipulate meme')
@allure.title('Удаление мема')
def test_delete(delete_meme_endpoint, new_meme_id, new_token):
    meme_id = new_meme_id
    print(f'Тест удаления объекта: {meme_id}')
    headers = {'Authorization': new_token}
    # Шаг 1: Проверяем, что мем существует ДО удаления
    with allure.step('Проверка существования мема перед удалением'):
        get_meme = GetMeme()
        get_meme.get_meme(meme_id, headers)
        get_meme.check_response_status_is_200()
        print(f'✓ Мем с ID {meme_id} существует')
    # Шаг 2: удаление
    delete_meme = DeleteMeme()
    delete_meme.delete_meme(meme_id, headers)
    delete_meme.check_response_status_is_200()
    # 3 Попытка повторного удаления
    with allure.step('Попытка повторного удаления'):
        delete_meme_again = DeleteMeme()
        delete_meme_again.delete_meme(meme_id, headers)

        # Проверяем, что получили 404
        delete_meme_again.check_not_found_404()
        print(f'✓ Получен ожидаемый статус 404 - мем уже удалён')


# ============ НЕГАТИВНЫЙ ТЕСТ 1: Невалидный ID мема ============
""" Негативный тест: попытка удалить мем с невалидным ID. Ожидается: 404 Not Found """
@pytest.mark.parametrize("invalid_id,test_description", [
    ("999999", "несуществующий_id"),
    ("abc", "буквенный_id"),
    ("", "пустой_id"),
    ("!@#$", "спецсимволы_в_id"),
    ("-1", "отрицательный_id"),
    ("0", "нулевой_id")
])
@allure.feature('Posts')
@allure.story('Manipulate post')
@allure.title('Удаление мема с невалидным ID')
@pytest.mark.negative
def test_delete_meme_with_invalid_id(delete_meme_endpoint, new_token, invalid_id, test_description):
    headers = {'Authorization': new_token}
    print(f'Тест удаления мема с {test_description}: {invalid_id}')

    with allure.step(f'Попытка удалить мем с {test_description}'):
        delete_meme = DeleteMeme()
        delete_meme.delete_meme(invalid_id, headers)

        # Проверяем, что получили 404
        delete_meme.check_not_found_404()
        print(f'✓ Получен статус {delete_meme.response.status_code} - для несуществующего мема')


# ============ НЕГАТИВНЫЙ ТЕСТ 2: Проблемный токен ============
""" Негативные тесты: попытка удалить мем с пустым, неправильным, отсутствующим токеном Ожидается: 401 """
@pytest.mark.parametrize("token_type,token_value,expected_status,test_description", [
    ("invalid", "invalid_token_12345", 401, "неправильный_токен"),
    ("missing", None, 401, "отсутствует_токен"),
    ("empty", "", 401, "пустой_токен")
])
@allure.feature('Posts')
@allure.story('Delete meme')
@allure.title('Удаление мема с проблемами авторизации')
@pytest.mark.negative
def test_delete_meme_auth_issues(delete_meme_endpoint, new_meme_id,
                                 token_type, token_value, expected_status, test_description):
    meme_id = new_meme_id
    # Формируем заголовки в зависимости от типа токена
    if token_value is None:
        headers = {}  # Нет токена вообще
    else:
        headers = {'Authorization': token_value}

    print(f'Тест удаления мема с {test_description}: {meme_id}')
    with allure.step(f'Попытка удалить мем с {test_description}'):
        delete_meme = DeleteMeme()
        delete_meme.delete_meme(meme_id, headers)

        # Проверяем, что получили 401
        delete_meme.check_bad_request_401()
        print(f'✓ Получен статус {delete_meme.response.status_code} - требуется авторизация')
