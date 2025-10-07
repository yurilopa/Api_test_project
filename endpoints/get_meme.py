import requests
import allure
from test_api_fin_project.endpoints.endpoint import Endpoint


class GetMeme(Endpoint):
    @allure.step('Get all meme')
    def get_all_meme(self, headers=None):
        self.response = requests.get(f'{self.url}/meme', headers=headers)
        print(f'GET response {self.response.status_code}')
        print(self.url)
        return self.response  # если потребуется вернуть данные json

    @allure.step('Check memes list is not empty')
    def check_memes_list_not_empty(self):
        memes = self.response.json()
        assert len(memes) > 0, "Список мемов пуст"
        print(f"Получено мемов: {len(memes)}")


    @allure.step('Get one meme')
    def get_meme(self, meme_id, headers=None):
        self.response = requests.get(f'{self.url}/meme/{meme_id}', headers=headers)
        print(f'GET response {self.response.status_code}')
        print(f'GET URL: {self.url}/meme/{meme_id}')
        return self.response


    @allure.step('Check id meme for test_get_one_meme')
    def check_meme_id(self, expected_id):
        assert self.response.json()['id'] == expected_id

