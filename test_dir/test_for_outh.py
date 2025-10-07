import pytest
import allure


# =============================================================================
# POSITIVE AUTHORIZATION TESTS (изменяем значение имени)
# =============================================================================
@pytest.mark.parametrize("name,test_name,expected_status", [
    ("ordinary", "ordinary_name", 200),
    ("Very long name " * 100, "long_name", 200),
    ("1234567890", "name_with_numbers", 200),
    ("", "empty_text", 200),
    ("!@#$%^&*()_+=~|{[]}'?/><`", "special_chars", 200),
    ("Привет мир! 🚀", "unicode", 200),
    ("'; DROP TABLE memes; --", "sql_injection", 200)
])
@allure.feature('Authorization')
@allure.story('Get Authorization Token')
@allure.title('Получение токена авторизации c разными параметрами в имени')
@pytest.mark.smoke
def test_create_token_check_name(create_token, name, test_name, expected_status):
    print(f'PUT запрос с {test_name}')
    allure.dynamic.title(f'Создание токена с {test_name}')
    with allure.step(f'Test PUT with {test_name}'):
        body =  {"name": name}
        headers = {'Content-Type': 'application/json'}
        response = create_token.create_new_token(body=body, headers=headers)
        print(f'Response status: {response.status_code}')
        print(f'Response text: {response.text}')
        # Проверяем статус
        assert response.status_code == expected_status, f"Ожидался {expected_status}, получен {response.status_code}"
        # Только для успешных запросов проверяем токен
        if expected_status == 200:
            # Проверка успешности запроса
            token = create_token.check_token_in_response()
            create_token.check_test_name(name, test_name)
            print(f'Token received: {token}')
        else:
            print(f'Негативный тест прошёл: получен ожидаемый код {expected_status}')


# =============================================================================
#NEGATIVE AUTHORIZATION TESTS
# =============================================================================
@allure.feature('Authorization')
@allure.story('Get Authorization Token')
@allure.title('Получение токена авторизации empty body')
@pytest.mark.smoke
def test_create_token_with_empty_body(create_token):
    body = {}
    headers = {'Content-Type': 'application/json'}
    response = create_token.create_new_token(body=body, headers=headers)
    print(f'Response status: {response.status_code}')
    print(f'Response text: {response.text}')
    # Проверка успешности запроса
    create_token.check_bad_request_400()


#NEGATIVE AUTHORIZATION TESTS (изменяем значение  в поле name)
@pytest.mark.parametrize("field_name,test_field_name,expected_status", [
    ("nam", "nam_in_field_name", 400),
    (" ", "space_in_field_name", 400),
    ("" , "empty_in_field_name", 400),
    ("1234567890", "numbers_in_field_name", 400),
    ("!@#$%^&*()_+=~|{[]}'?/><`", "special_chars_in_field_name", 400),
    ("Привет мир! 🚀", "unicode_in_field_name", 400),
    ("'; DROP TABLE memes; --", "sql_injection_in_field_name", 400)
])
@allure.feature('Authorization')
@allure.story('Get Authorization Token')
@allure.title('Получение токена авторизации c разными параметрами в элементе имя')
@pytest.mark.smoke
def test_create_token_check_field_name(create_token, field_name, test_field_name, expected_status):
    print(f'PUT запрос с {test_field_name}')
    allure.dynamic.title(f'Создание токена с {test_field_name}')
    with allure.step(f'Test PUT with {test_field_name}'):
        body =  {field_name: "name"}
        headers = {'Content-Type': 'application/json'}
        response = create_token.create_new_token(body=body, headers=headers)
        print(f'Response status: {response.status_code}')
        print(f'Response text: {response.text}')
        # Проверяем статус
        assert response.status_code == expected_status, f"Ожидался {expected_status}, получен {response.status_code}"
        # Только для успешных запросов проверяем токен
        if expected_status == 200:
            # Проверка успешности запроса
            token = create_token.check_token_in_response()
            create_token.check_test_name(field_name, test_field_name)
            print(f'Token received: {token}')
        else:
            print(f'Негативный тест прошёл: получен ожидаемый код {expected_status}')


"""запрос, с неправильным Content-Type"""
@allure.feature('Memes')
@allure.story('Manipulate memes')
@allure.title('запрос, с неправильным Content-Type')
@pytest.mark.medium
def test_put_meme_text_headers(create_token):  # get_meme_endpoint, update_meme_endpoint, new_meme_id, new_token):
    print('запрос, с неправильным Content-Type')
    body = {"name": "name"}
    headers = {'Content-Type': 'text/plain'}
    with allure.step('Test with wrong Content-Type'):
        response = create_token.create_new_token(body=body, headers=headers)
        print(f'Response status: {response.status_code}')
        print(f'Response text: {response.text}')
        # Проверка успешности запроса
        create_token.check_bad_request_500()


"""запрос, с неправильным Content-Type"""
@allure.feature('Memes')
@allure.story('Manipulate memes')
@allure.title('запрос, с неправильным Content-Type - multipart/form-data')
@pytest.mark.medium
def test_put_meme_multipart_headers(create_token):  # get_meme_endpoint, update_meme_endpoint, new_meme_id, new_token):
    print('запрос, с неправильным Content-Type - multipart/form-data')
    body = {"name": "name"}
    headers = {'Content-Type': 'multipart/form-data'}
    with allure.step('Test with wrong Content-Type'):
        response = create_token.create_new_token(body=body, headers=headers)
        print(f'Response status: {response.status_code}')
        print(f'Response text: {response.text}')
        # Проверка успешности запроса
        create_token.check_bad_request_500()


@pytest.mark.parametrize("content_type,expected_status", [
    ("application/json", 200),  # Правильный формат
    ("multipart/form-data", 415),  # Неправильный формат - ожидаем 415
    ("text/plain", 415),  # Другой неправильный формат
    ("application/xml", 415),  # Ещё один неправильный формат
])
@allure.feature('Authorization')
@allure.story('Content-Type validation')
@allure.title('Проверка валидации Content-Type')
def test_create_token_different_content_types(create_token, content_type, expected_status):
    print(f'PUT запрос с Content-Type: {content_type}')
    allure.dynamic.title(f'Создание токена с Content-Type: {content_type}')

    with allure.step(f'Test PUT with Content-Type: {content_type}'):
        body = {"name": "test_user"}
        headers = {'Content-Type': content_type}

        response = create_token.create_new_token(body=body, headers=headers)

        print(f'Response status: {response.status_code}')
        print(f'Response text: {response.text}')
        print(f'Response headers: {response.headers}')

        # Проверяем статус
        assert response.status_code == expected_status, f"Ожидался {expected_status}, получен {response.status_code}"
        # Только для успешных запросов проверяем токен
        if expected_status == 200:
            # Проверка успешности запроса
            token = create_token.check_token_in_response()
            create_token.check_test_headers(content_type)
            print(f'Token received: {token}')
        else:
            print(f'Негативный тест прошёл: получен ожидаемый код {expected_status}')