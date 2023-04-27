import requests


class UserInfo:
    providers = None

    def __init__(self, provider_name):
        self.data = None
        self.provider_name = provider_name

    @classmethod
    def get_provider(cls, provider_name):
        if cls.providers is None:
            cls.providers = {}
            for provider_class in cls.__subclasses__():
                provider = provider_class()
                cls.providers[provider.provider_name] = provider
        return cls.providers[provider_name]


class UserInfoVK(UserInfo):
    def __init__(self, user_id, token):
        super().__init__('vk')
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


class UserInfoGoogle(UserInfo):
    def __init__(self, token):
        super().__init__('google')
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
