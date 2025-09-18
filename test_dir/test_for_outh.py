import pytest
import allure


# =============================================================================
# POSITIVE AUTHORIZATION TESTS (изменяем значение имени)
# =============================================================================
@allure.feature('Authorization')
@allure.story('Get Authorization Token')
@allure.title('Получение токена авторизации')
@pytest.mark.smoke
def test_create_token(create_token):
    body = {"name": "Yuri Tester"}
    headers = {'Content-Type': 'application/json'}
    response = create_token.create_new_token(body=body, headers=headers)
    print(f'Response status: {response.status_code}')
    print(f'Response text: {response.text}')
    # Проверка успешности запроса
    create_token.check_response_status_is_200()

@allure.feature('Authorization')
@allure.story('Get Authorization Token')
@allure.title('Получение токена авторизации с цифрами в имени')
@pytest.mark.smoke
def test_create_token_with_name_int(create_token):
    body = {"name": "1234567890987654321"}
    headers = {'Content-Type': 'application/json'}
    response = create_token.create_new_token(body=body, headers=headers)
    print(f'Response status: {response.status_code}')
    print(f'Response text: {response.text}')
    # Проверка успешности запроса
    create_token.check_response_status_is_200()

@allure.feature('Authorization')
@allure.story('Get Authorization Token')
@allure.title('Получение токена авторизация с 1 символом в имени')
@pytest.mark.smoke
def test_create_token_with_one_sim_in_name(create_token):
    body = {"name": "1"}
    headers = {'Content-Type': 'application/json'}
    response = create_token.create_new_token(body=body, headers=headers)
    print(f'Response status: {response.status_code}')
    print(f'Response text: {response.text}')
    # Проверка успешности запроса
    create_token.check_response_status_is_200()


# =============================================================================
# BOUNDARY TESTS
# =============================================================================
@allure.feature('Authorization')
@allure.story('Get Authorization Token')
@allure.title('Получение токена авторизации с граничными значениями длины полей')
@pytest.mark.medium
def test_authorization_with_long_name(create_token):
    print('Получение токена авторизации с граничными значениями длины полей')
    long_username = 'long name' * 1000
    body = {"name": long_username}
    headers = {'Content-Type': 'application/json'}
    response = create_token.create_new_token(body=body, headers=headers)
    print(f'Response status: {response.status_code}')
    print(f'Response text: {response.text}')
    # Проверка успешности запроса
    create_token.check_response_status_is_200()

@allure.feature('Authorization')
@allure.story('Get Authorization Token')
@allure.title('Получение токена авторизации, спец символы в имени')
@pytest.mark.smoke
def test_create_token_with_spec_characters(create_token):
    body = {"name": "!@#$%^&*"}
    headers = {'Content-Type': 'application/json'}
    response = create_token.create_new_token(body=body, headers=headers)
    print(f'Response status: {response.status_code}')
    print(f'Response text: {response.text}')
    # Проверка успешности запроса
    create_token.check_response_status_is_200()

@allure.feature('Authorization')
@allure.story('Get Authorization Token')
@allure.title('Получение токена авторизации, пусто в имени')
@pytest.mark.smoke
def test_create_token_with_empty_name(create_token):
    body = {"name": ""}
    headers = {'Content-Type': 'application/json'}
    response = create_token.create_new_token(body=body, headers=headers)
    print(f'Response status: {response.status_code}')
    print(f'Response text: {response.text}')
    # Проверка успешности запроса
    create_token.check_response_status_is_200()

@allure.feature('Authorization')
@allure.story('Get Authorization Token')
@allure.title('Получение токена авторизации, пробел в имени')
@pytest.mark.smoke
def test_create_token_with_probel_name(create_token):
    body = {"name": " "}
    headers = {'Content-Type': 'application/json'}
    response = create_token.create_new_token(body=body, headers=headers)
    print(f'Response status: {response.status_code}')
    print(f'Response text: {response.text}')
    # Проверка успешности запроса
    create_token.check_response_status_is_200()

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
@allure.feature('Authorization')
@allure.story('Get Authorization Token')
@allure.title('Получение токена авторизации с измененным полем name')
@pytest.mark.smoke
def test_create_token_where_name_nam(create_token):
    body = {"nam": "Yuri Tester"}
    headers = {'Content-Type': 'application/json'}
    response = create_token.create_new_token(body=body, headers=headers)
    print(f'Response status: {response.status_code}')
    print(f'Response text: {response.text}')
    # Проверка успешности запроса
    create_token.check_bad_request_400()

@allure.feature('Authorization')
@allure.story('Get Authorization Token')
@allure.title('Получение токена авторизации с цифрами в имени')
@pytest.mark.smoke
def test_create_token_where_name_int(create_token):
    body = {"1234567890987654321": "Yuri"}
    headers = {'Content-Type': 'application/json'}
    response = create_token.create_new_token(body=body, headers=headers)
    print(f'Response status: {response.status_code}')
    print(f'Response text: {response.text}')
    # Проверка успешности запроса
    create_token.check_bad_request_400()

@allure.feature('Authorization')
@allure.story('Get Authorization Token')
@allure.title('Успешное получение токена авторизации спец символы в имени')
@pytest.mark.smoke
def test_create_token_where_spec_name(create_token):
    body = {"@#$%^&*": "Yuri"}
    headers = {'Content-Type': 'application/json'}
    response = create_token.create_new_token(body=body, headers=headers)
    print(f'Response status: {response.status_code}')
    print(f'Response text: {response.text}')
    # Проверка успешности запроса
    create_token.check_bad_request_400()

@allure.feature('Authorization')
@allure.story('Get Authorization Token')
@allure.title('Успешное получение токена авторизации пусто в имени')
@pytest.mark.smoke
def test_create_token_where_empty_name(create_token):
    body = {"": "name"}
    headers = {'Content-Type': 'application/json'}
    response = create_token.create_new_token(body=body, headers=headers)
    print(f'Response status: {response.status_code}')
    print(f'Response text: {response.text}')
    # Проверка успешности запроса
    create_token.check_bad_request_400()

@allure.feature('Authorization')
@allure.story('Get Authorization Token')
@allure.title('Успешное получение токена авторизации пробел в имени')
@pytest.mark.smoke
def test_create_token_where_probel_in_name(create_token):
    body = {" ": "name"}
    headers = {'Content-Type': 'application/json'}
    response = create_token.create_new_token(body=body, headers=headers)
    print(f'Response status: {response.status_code}')
    print(f'Response text: {response.text}')
    # Проверка успешности запроса
    create_token.check_bad_request_400()

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