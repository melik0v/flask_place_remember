import requests


class UserInfoVK:
    def __init__(self, user_id, token):
        self.data = {'user_id': user_id,
                     'v': '5.131',
                     'fields': 'photo',
                     'access_token': token,
                     }

    def get_avatar(self):
        response = requests.get('https://api.vk.com/method/users.get', params=self.data)
        if response.json():
            avatar = response.json().get('response')[0]['photo']
            return avatar
        return None

    def get_firstname_lastname(self):
        response = requests.get('https://api.vk.com/method/users.get', params=self.data)
        if response.json():
            user_info = response.json().get('response')[0]
            first_name, last_name = user_info['first_name'], user_info['last_name']
            return first_name, last_name
        return None


class UserInfoGoogle:
    def __init__(self, token):
        self.data = {
            'access_token': token,
        }

    def get_avatar(self):
        response = requests.get('https://www.googleapis.com/oauth2/v1/userinfo?alt=json', params=self.data)
        if response.json():
            avatar = response.json()['picture']
            return avatar
        return None

    def get_firstname_lastname(self):
        response = requests.get('https://www.googleapis.com/oauth2/v1/userinfo?alt=json', params=self.data)
        if response.json():
            user_info = response.json()
            first_name, last_name = user_info['given_name'], user_info['family_name']
            return first_name, last_name
        return None
