import requests
import allure
from test_api_fin_project.endpoints.endpoint import Endpoint


class GetMeme(Endpoint):
    @allure.step('Get all meme')
    def get_all_meme(self):
        self.response = requests.get(self.url)
        print(f'GET response {self.response.status_code}')
        print(self.url)
        return self.response  # если потребуется вернуть данные json

    @allure.step('Get one meme')
    def get_meme(self, meme_id, headers=None):
        self.response = requests.get(f'{self.url}/{meme_id}', headers=headers)
        print(f'GET response {self.response.status_code}')
        print(f'GET URL: {self.url}/{meme_id}')
        return self.response

    @allure.step('Check status code')
    def check_status_code(self, expected_status=200):
        assert self.response.status_code == expected_status

    @allure.step('Check id meme for test_get_one_meme')
    def check_meme_id(self, expected_id):
        assert self.response.json()['id'] == expected_id

