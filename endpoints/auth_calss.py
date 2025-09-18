import requests
import allure
from test_api_fin_project.endpoints.endpoint import Endpoint


class GetToken(Endpoint):
    #url = 'http://memesapi.course.qa-practice.com/authorize'
    @allure.step('Test auth endpoint')
    def create_new_token(self, body, headers):
        self.response = requests.post(f'{self.url}/authorize', json=body, headers=headers)
        print(self.response, self.url)
        return self.response
