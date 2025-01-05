import os.path
from pprint import pprint
import requests
from dotenv import load_dotenv

dotenv_path = 'config_MY.env'
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

vk_token = os.getenv('VK_token')
ya_token = os.getenv('YA_token')

class VKconnector:
    def __init__(self, access_token, version='5.199'):
        self.access_token = access_token
        self.version = version
        self.base_url = 'https://api.vk.com/method/'
        self.params = {
                        'access_token': self.access_token,
                        'v': self.version   
        }

    def user_info(self, user_id):
        url = f'{self.base_url}users.get'
        params = {
            **self.params,
            'user_ids': user_id
        }
        response = requests.get(url, params=params)
        return response.json()
    
    def friends_info(self, user_id, count = 5):
        url = f'{self.base_url}friends.get'
        params = {
            **self.params,
            'user_id': user_id,
            'count': count,
            'fields': ['nickname']
        }
        response = requests.get(url, params=params)
        return response.json()
    
    def photos_info(self, user_id,):
        url = f'{self.base_url}photos.get'
        params = {
            **self.params,
            'owner_id': user_id,
            'album_id': 'profile'
            
        }
        response = requests.get(url, params=params)
        return response.json()


class YAconnector:
    def __init__ (self, token):
        self.headers = {'Authorization': f'OAuth {token}'}

    def create_folder(self, folder_name):
        response = requests.put(url = 'https://cloud-api.yandex.net/v1/disk/resources',
                                headers = self.headers,
                                params={'path': folder_name})
        return response.status_code


       # pprint(response.status_code)
        #pprint(response.json())

#current_drive = "YA"
#drive_connector = None
#if current_drive == "YA":
#    drive_connector = YAconnector(ya_token)
#drive_connector.create_folder('itogovaya rabota')
 



connector = VKconnector(vk_token)
#user_info = connector.user_info(20334095)
#friends_info = connector.friends_info(20334095)
#pprint(user_info)
#pprint(friends_info)
#photos_info = connector.photos_info(20334095)
#pprint(photos_info)

ya_connector = YAconnector(ya_token)
ya_connector.create_folder('itogovaya rabota')