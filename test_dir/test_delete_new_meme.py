import allure
from test_api_fin_project.endpoints.delete_meme import (DeleteMeme)


@allure.feature('Posts')
@allure.story('Manipulate post')
@allure.title('Удаление мема')
def test_delete(delete_meme_endpoint, new_meme_id, new_token):
    meme_id = new_meme_id
    print('Тест удаления объекта')
    headers = {'Authorization': new_token}
    delete_meme = DeleteMeme()
    delete_meme.delete_meme(meme_id, headers)
    delete_meme.check_response_status_is_200()
