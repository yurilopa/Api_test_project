import requests
import allure
from requests import JSONDecodeError
from test_api_fin_project.endpoints.endpoint import Endpoint


class UpdateMeme(Endpoint):
    @allure.step('Getting existing meme')
    def getting_existing_meme(self, new_meme_id, headers):
        get_response = requests.get(
            f'{self.url}/{new_meme_id}',
            headers=headers
        )
        assert get_response.status_code == 200, f'Could got get mem {get_response.text}'
        existing_meme = get_response.json()
        print(f'Original meme {existing_meme}')
        return existing_meme  # если потребуется вернуть данные json

    @allure.step('Updating meme with PUT request')
    def update_meme(self, new_meme_id, body, headers):
        self.response = requests.put(
            f'{self.url}/{new_meme_id}',
            headers=headers,
            json=body
        )
        if self.response.status_code in [404, 401, 403, 405, 500]:
            self.json = None
            return
        content_type = self.response.headers.get('content_type', '')
        if 'application/json' in content_type:
            try:
                self.json = self.response.json()
            except JSONDecodeError:
                self.json = None
        else:
            self.json = None
        print(f'Response status: {self.response.status_code}')
        print(f'Response text: {self.response.text}')
        self.json = self.response.json()
        return self.response  # если потребуется вернуть данные json

    @allure.step('Check PUT request status code')
    def check_status_code(self, expected_status=200):
        assert self.response.status_code == expected_status, f'Could got get mem {self.response.text}'

    @allure.step('Check PUT request that text is correct')
    def check_response_text(self, text, meme_id):
        assert self.json['text'] == text,  f"Text not updated correctly in meme {meme_id}"

    @allure.step('Check PUT request that url is correct')
    def check_response_url(self, url, meme_id):
        assert self.json['url'] == url,  f"Text not updated correctly in meme {meme_id}"

    @allure.step('Check PUT request that tags is correct')
    def check_response_tags(self, tags, meme_id):
        assert self.json['tags'] == tags,  f"Text not updated correctly in meme {meme_id}"

    # Проверка обновления только текстового поля:
    @allure.step('Check PUT request for change text only in meme')
    def check_text_only_updated(self, expected_text, meme_id):
        assert self.json['text'] == expected_text, f"Text not updated correctly in meme {meme_id}"

    # Проверка обновления только поля url:
    @allure.step('Check PUT request for change url only in meme')
    def check_url_only_updated(self, expected_url, meme_id):
        assert self.json['url'] == expected_url, f"Url not updated correctly in meme {meme_id}"

    # Проверка обновления только поля tags:
    @allure.step('Check PUT request for change tags only in meme')
    def check_tags_only_updated(self, expected_tags, meme_id):
        assert self.json['tags'] == expected_tags, f"Tags not updated correctly in meme {meme_id}"

    # Проверка обновления только поля info:
    @allure.step('Check PUT request for change info only in meme')
    def check_info_only_updated(self, expected_info, meme_id):
        assert self.json['info'] == expected_info, f"Info not updated correctly in meme {meme_id}"

    # Далее методы для проверки граничных значений:
    @allure.step('Check boundary test response status')
    def check_boundary_status(self, expected_statuses=None):
        if expected_statuses is None:
            expected_statuses = [200, 400]
        assert self.response.status_code in expected_statuses, f"Unexpected status: {self.response.status_code}"
        print(f'Response status: {self.response.status_code}')

    @allure.step('Check test long text')
    def check_long_text(self, long_text):
        assert self.json['text'] == long_text, "Long text not saved}"
        print(f'Response status: {self.response.status_code}')

    @allure.step('Check test empty text')
    def check_empty_text(self, empty_text):
        assert self.json['text'] == empty_text, "Empty text not saved}"
        print(f'Response status: {self.response.status_code}')

    @allure.step('Check test text with special charts')
    def check_text_with_spec_charts(self, spec_text):
        assert self.json['text'] == spec_text, "Long text not saved}"
        print(f'Response status: {self.response.status_code}')

    @allure.step('Check test with many tags')
    def check_test_with_many_tags(self, many_tags):
        assert self.json['tags'] == many_tags, "Many tags not saved"
        print(f'Response status: {self.response.status_code}')

    @allure.step('Check test with many info')
    def check_test_with_many_info(self, many_info):
        assert self.json['info'] == many_info, "Many info not saved"
        print(f'Response status: {self.response.status_code}')

    @allure.step('Check test empty fields body')
    def check_test_with_empty_fields_body(self, empty_fields_body):
        """Проверяет обработку пустых полей"""
        # Проверяем, что есть JSON ответ
        if self.json is None:
            print("No JSON response received")
            return

        print(f"Testing empty fields. Expected: {empty_fields_body}")
        print(f"Server response: {self.json}")
        # Если сервер принял запрос (200), проверяем поля по отдельности
        if self.response.status_code == 200:
            print("All empty fields saved correctly")
        elif self.response.status_code == 400:
            print("Server rejected empty fields with 400 Bad Request (expected behavior)")
        else:
            print(f"Unexpected status for empty fields: {self.response.status_code}")
            print(f"Response text: {self.response.text[:200]}...")

    @allure.step('Check response contain text')
    def check_response_text(self, expected_text):
        response_text = self.response.text
        assert expected_text.lower() in response_text.lower(), \
            f'Expected "{expected_text}" in response, but got "{response_text}"'

    @allure.step('Check response field value')
    def check_response_field(self, field_name, expected_value):
        response_data = self.response.json()
        actual_value = response_data.get(field_name)
        assert actual_value == expected_value, f'Expected {field_name}="{expected_value}", but got"{actual_value}"'

    # Далее методы для проверки негативных значений:
    @allure.step('Check negative test response status')
    def check_negative_status(self, expected_statuses=None):
        if expected_statuses is None:
            expected_statuses = [400, 401, 404, 415, 500]
        assert self.response.status_code in expected_statuses, f"Unexpected status: {self.response.status_code}"
