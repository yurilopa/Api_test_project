import requests
import allure
from requests import JSONDecodeError
from test_api_fin_project.endpoints.endpoint import Endpoint
from test_api_fin_project.endpoints.get_meme import GetMeme  # Импортируем существующий класс


class UpdateMeme(Endpoint):
    def __init__(self):
        super().__init__()
        self.get_meme = GetMeme()  # Композиция для получения мемов


    @allure.step('Updating meme with PUT request')
    def update_meme(self, new_meme_id, body, headers):
        self.response = requests.put(
            f'{self.url}/meme/{new_meme_id}',
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


    @allure.step('Check test text')
    def check_test_text(self, expected_text, test_type="text"):
        assert self.json['text'] == expected_text, "text not saved"
        print(f'Response status: {self.response.status_code}')
        # Дополнительное логирование в зависимости от типа теста
        if test_type == "long_text":
            print(f'Long text saved successfully! Length: {len(expected_text)} characters')
        elif test_type == "empty_text":
            print('Empty text saved successfully!')
        elif test_type == "special_chars":
            print('Special characters text saved successfully!')
        else:
            print(f'{test_type} text saved successfully!')

    # Проверка обновления с большим кол-вом тегов:
    @allure.step('Check test with many tags')
    def check_test_with_many_tags(self, many_tags):
        assert self.json['tags'] == many_tags, "Many tags not saved"
        print(f'Response status: {self.response.status_code}')


    # Проверка обновления с большим кол-вом info:
    @allure.step('Check test with many info')
    def check_test_with_many_info(self, many_info):
        assert self.json['info'] == many_info, "Many info not saved"
        print(f'Response status: {self.response.status_code}')


    # Проверка обновления с пустыми данными в боди:
    @allure.step('Check test empty fields body')
    def check_test_with_empty_fields_body(self, empty_fields_body):
        """Проверяет обработку пустых полей"""
        # Проверяем, что есть JSON ответ
        if self.json is None:
            print("No JSON response received")
            return


    @allure.step('Check response contain text')
    def check_response_text(self, expected_text):
        response_text = self.response.text
        assert expected_text.lower() in response_text.lower(), \
            f'Expected "{expected_text}" in response, but got "{response_text}"'
