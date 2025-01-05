import requests
from pprint import pprint
class VK:
    def __init__(self, access_token, user_id, version='5.199'):
        self.token = access_token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def users_info(self):
        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': self.id}
        response = requests.get(url, params={**self.params, **params})
        return response.json()

access_token = 'vk1.a.dHr3AW09m6zvJ3up6Lv7Le8hTiV0hYDtTuZU7oQbWtJOa8yQ6d67GYxsSQG8Mb-aZaoiF8gKs9v-e8lH6VkhtbBZI0pdCTnMj7PNl0REI8sRi3IgSVioGrA6rWDI2ThIsUk0VWQbLn45BwP7doTMVvBj-xPvexgnSAkVN3M8Ek4-EBswI8v_l-dnlPbMAN_6&'
user_id = '20334095'
vk = VK(access_token, user_id)
pprint(vk.users_info())
