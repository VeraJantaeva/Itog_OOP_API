import os.path
from pprint import pprint
import requests
from dotenv import load_dotenv
import json
import datetime
import time
from tqdm import tqdm



dotenv_path = 'config_MY.env'
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

vk_token = os.getenv('VK_token')
ya_token = os.getenv('YA_token')
user_id = os.getenv('ID')
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
    
    # def friends_info(self, user_id, count = 5):
    #     url = f'{self.base_url}friends.get'
    #     params = {
    #         **self.params,
    #         'user_id': user_id,
    #         'count': count,
    #         'fields': ['nickname']
    #     }
    #     response = requests.get(url, params=params)
    #     return response.json()
    
    def photos_info(self, user_id):
        url = f'{self.base_url}photos.get'
        params = {
            **self.params,
            'owner_id': user_id,
            'album_id': 'profile'   
        }
        photo_info = requests.get(url, params=params).json()
        return photo_info
    
    def _get_logs_only(self):
        """Метод для получения словаря с параметрами фотографий"""
        photo_count, photo_items = self._get_photo_info()
        result = {}
        for i in range(photo_count):
            likes_count = photo_items[i]['likes']['count']
            url_download, picture_size = find_max_dpi(photo_items[i]['sizes'])
            time_warp = time_convert(photo_items[i]['date'])
            new_value = result.get(likes_count, [])
            new_value.append({'likes_count': likes_count,
                              'add_name': time_warp,
                              'url_picture': url_download,
                              'size': picture_size})
            result[likes_count] = new_value
        return result

    def _sort_info(self):
        """Метод для получения словаря с параметрами фотографий и списка JSON для выгрузки"""
        json_list = []
        sorted_dict = {}
        picture_dict = self._get_logs_only()
        counter = 0
        for elem in picture_dict.keys():
            for value in picture_dict[elem]:
                if len(picture_dict[elem]) == 1:
                    file_name = f'{value["likes_count"]}.jpeg'
                else:
                    file_name = f'{value["likes_count"]} {value["add_name"]}.jpeg'
                json_list.append({'file name': file_name, 'size': value["size"]})
                if value["likes_count"] == 0:
                    sorted_dict[file_name] = picture_dict[elem][counter]['url_picture']
                    counter += 1
                else:
                    sorted_dict[file_name] = picture_dict[elem][0]['url_picture']
        return json_list, sorted_dict


class YAconnector:
    def __init__ (self, folder_name):
        self.headers = {'Authorization': f'OAuth {ya_token}'}
    
        self.url = "https://cloud-api.yandex.net/v1/disk/resources/upload"

        self.folder = self.create_folder(folder_name)

    def create_folder(self, folder_name):
        response = requests.put(url = 'https://cloud-api.yandex.net/v1/disk/resources',
                                headers = self.headers,
                                params={'path': folder_name})
        return response.status_code
    
    def _in_folder(self, folder_name):
        """Метод для получения ссылки для загрузки фотографий на Я-диск"""
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        params = {'path': folder_name}
        resource = requests.get(url, headers=self.headers, params=params).json()
        in_folder_list = []
        for elem in resource:
            in_folder_list.append(elem)
        return in_folder_list

    def create_copy(self, dict_files):
        """Метод загрузки фотографий на Я-диск"""
        files_in_folder = self._in_folder(self.folder)
        copy_counter = 0
        for key, i in zip(dict_files.keys(), tqdm(range(self.added_files_num))):
            if copy_counter < self.added_files_num:
                if key not in files_in_folder:
                    params = {'path': f'{self.folder}/{key}',
                              'url': dict_files[key],
                              'overwrite': 'false'}
                    requests.post(self.url, headers=self.headers, params=params)
                    copy_counter += 1
                else:
                    print(f'Внимание:Файл {key} уже существует')
            else:
                break

def find_max_dpi(dict_in_search):
    """Функция возвращает ссылку на фото максимального размера и размер фото"""
    max_dpi = 0
    need_elem = 0
    for j in range(len(dict_in_search)):
        file_dpi = dict_in_search[j].get('width') * dict_in_search[j].get('height')
        if file_dpi > max_dpi:
            max_dpi = file_dpi
            need_elem = j
    return dict_in_search[need_elem].get('url'), dict_in_search[need_elem].get('type')

def time_convert(time_unix):
    """Функция преобразует дату загрузки фото в привычный формат"""
    time_bc = datetime.datetime.fromtimestamp(time_unix)
    str_time = time_bc.strftime('%Y-%m-%d time %H-%M-%S')
    return str_time

def create_folder(self, folder_name):
        response = requests.put(url = 'https://cloud-api.yandex.net/v1/disk/resources',
                                headers = self.headers,
                                params={'path': folder_name})
        return response.status_code


# connector = VKconnector(vk_token)
# photo_info = connector.photos_info(20334095)
# pprint(photo_info)



# ya_connector = YAconnector(ya_token)
# ya_connector.create_folder('itogovaya rabota')

if __name__ == '__main__':

    connector = VKconnector(vk_token)
    photo_info = connector.photos_info(user_id)
    with open('my_VK_photo.json', 'w') as f:  # Сохранение JSON списка в файл my_VK_photo.json
        json.dump(photo_info, f)

    # Создаем экземпляр класса Yandex с параметрами: "Имя папки", "Токен" и количество скачиваемых файлов
    
    ya_connector = YAconnector(ya_token)
    ya_connector.create_folder('VK photo uplouds')
    
    ya_connector.create_copy(connector.photos_info)  # Вызываем метод create_copy для копирования фотографий с VK на Я-диск