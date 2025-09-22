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


    @allure.step('Negative test auth endpoint')
    def check_token_in_response(self):
        response_data = self.response.json()
        with allure.step('check token'):
            assert 'token' in response_data, f'token not found in response {response_data}'
            assert response_data['token'] is not None, 'Token is None'
            assert response_data['token'] != "", "Token is empty string"
        return response_data['token']
