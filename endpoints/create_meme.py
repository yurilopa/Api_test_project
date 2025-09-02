import requests
import allure
from test_api_fin_project.endpoints.endpoint import Endpoint


class CreateMeme(Endpoint):
    @allure.step('Creating meme')
    def create_new_meme(self, body, headers):
        self.response = requests.post(
            self.url,
            json=body,
            headers=headers
        )
        print(self.response, self.url)
        self.json = self.response.json()
        return self.response  # если потребуется вернуть данные json

    @allure.step('Check status code')
    def check_status_code(self, expected_status=200):
        assert self.response.status_code == expected_status

    @allure.step('Check that text is correct')
    def check_response_text(self, text, meme_id):
        assert self.json['text'] == text,  f"Text not updated correctly in meme {meme_id}"

    @allure.step('Check that url is correct')
    def check_response_url(self, url, meme_id):
        assert self.json['url'] == url,  f"Text not updated correctly in meme {meme_id}"

    @allure.step('Check that tags is correct')
    def check_response_tags(self, tags, meme_id):
        assert self.json['tags'] == tags,  f"Text not updated correctly in meme {meme_id}"
