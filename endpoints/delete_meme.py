import requests
import allure
from test_api_fin_project.endpoints.endpoint import Endpoint


class DeleteMeme(Endpoint):
    @allure.step('Delete meme')
    def delete_meme(self, meme_id, headers):
        self.response = requests.delete(f'{self.url}/{meme_id}', headers=headers)
        print(f'DELETE response {self.response.status_code}')
        print(f'DELETE URL: {self.url}/{meme_id}')
        return self.response

    @allure.step('Check status code')
    def check_status_code(self, expected_status=200):
        assert self.response.status_code == expected_status

    @allure.step('Check id meme for test_delete_meme')
    def check_meme_id(self, expected_id):
        assert self.response.json()['id'] == expected_id