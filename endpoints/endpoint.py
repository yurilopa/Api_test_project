import allure


class Endpoint:
    def __init__(self):
        self.url = "http://memesapi.course.qa-practice.com"  # meme"  # Атрибут экземпляра
        self.headers = {'Content-Type': 'application/json'}       # Атрибут экземпляра
        self.response = None
        self.json = None
        self.meme_id = None


    @allure.step('Check that title is the same sent')
    def check_response_name_is_correct(self, name):
        assert self.json['name'] == name, 'name is not name'


    @allure.step('Check that response is 200')
    def check_response_status_is_200(self):
        assert self.response.status_code == 200, f"Ожидался код 200, получен {self.response.status_code}"


    @allure.step('Check that 400 error received')
    def check_bad_request_400(self):
        assert self.response.status_code == 400, f"Ожидался код 400, получен {self.response.status_code}"


    @allure.step('Check that 401 error received')
    def check_bad_request_401(self):
        assert self.response.status_code == 401, f"Ожидался код 401, получен {self.response.status_code}"


    @allure.step('Check that 403 error received')
    def check_bad_request_403(self):
        assert self.response.status_code == 403, f"Ожидался код 403, получен {self.response.status_code}"


    @allure.step('Check that 404 error received')
    def check_bad_request_404(self):
        assert self.response.status_code == 404, f"Ожидался код 404, получен {self.response.status_code}"


    @allure.step('Check that 405 error received')
    def check_bad_request_405(self):
        assert self.response.status_code == 405, f"Ожидался код 405, получен {self.response.status_code}"


    @allure.step('Check that 415 error received')
    def check_bad_request_415(self):
        assert self.response.status_code == 415, f"Ожидался код 415, получен {self.response.status_code}"


    @allure.step('Check that 500 error received')
    def check_bad_request_500(self):
        assert self.response.status_code == 500, f"Ожидался код 500, получен {self.response.status_code}"
