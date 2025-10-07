import requests
import allure


from test_api_fin_project.endpoints.endpoint import Endpoint


class GetToken(Endpoint):
    @allure.step('Test auth endpoint')
    def create_new_token(self, body, headers):
        self.response = requests.post(f'{self.url}/authorize', json=body, headers=headers)
        print(self.response, self.url)
        return self.response


    @allure.step('Test auth endpoint')
    def check_token_in_response(self):
        response_data = self.response.json()
        with allure.step('check token'):
            assert 'token' in response_data, f'token not found in response {response_data}'
            assert response_data['token'] is not None, 'Token is None'
            assert response_data['token'] != "", "Token is empty string"
        return response_data['token']


    def get_token_from_response(self):
        """Возвращает токен из ответа"""
        return self.response.json().get("token")


    @allure.step('Check test name')
    def check_test_name(self, expected_text, name_type="name"):
        response_data = self.response.json()  # Получаем JSON
        assert response_data['user'] == expected_text, f"Ожидал '{expected_text}', отдал '{response_data.get('user')}'"
        print(f'Response status: {self.response.status_code}')
        # Дополнительное логирование в зависимости от типа теста
        if name_type == "long_name":
            print(f'Long name saved successfully! Length: {len(expected_text)} characters')
        elif name_type == "empty_name":
            print('Empty name saved successfully!')
        elif name_type == "special_chars":
            print('Special characters name saved successfully!')
        else:
            print(f'{name_type} name saved successfully!')


    @allure.step('Check test field name')
    def check_test_field_name(self, expected_text, name_type="name"):
        response_data = self.response.json()  # Получаем JSON
        assert response_data['user'] == expected_text, f"Ожидал '{expected_text}', отдал '{response_data.get('user')}'"
        print(f'Response status: {self.response.status_code}')
        # Дополнительное логирование в зависимости от типа теста
        if name_type == "long_name":
            print(f'Long name saved successfully! Length: {len(expected_text)} characters')
        elif name_type == "empty_name":
            print('Empty name saved successfully!')
        elif name_type == "special_chars":
            print('Special characters name saved successfully!')
        else:
            print(f'{name_type} name saved successfully!')


    @allure.step('Check test name')
    def check_test_headers(self, expected_text, name_type="name"):
        # assert self.json['name'] == expected_text, "token not found"
        response_data = self.response.json()  # Получаем JSON
        assert response_data['user'] == expected_text, f"Ожидал '{expected_text}', отдал '{response_data.get('user')}'"
        print(f'Response status: {self.response.status_code}')
        # Дополнительное логирование в зависимости от типа теста
        if name_type == "application/json":
            print(f'application/json: {len(expected_text)}')
        elif name_type == "multipart/form-data":
            print('multipart/form-data saved successfully!')
        elif name_type == "text/plain":
            print('text/plain saved successfully!')
        elif name_type == "application/xml":
            print('application/xml saved successfully!')
        else:
            print(f'{name_type} name saved successfully!')
