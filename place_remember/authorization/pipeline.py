from rauth import OAuth2Service
from flask import (
    current_app,
    url_for,
    redirect,
    request,
)
import requests


class OAuthSignIn(object):
    providers = None
    service = None

    def __init__(self, provider_name):
        self.provider_name = provider_name
        credentials = current_app.config["OAUTH_CREDENTIALS"][provider_name]
        self.consumer_id = credentials["id"]
        self.consumer_secret = credentials["secret"]

    def authorize(self):
        return redirect(
            self.service.get_authorize_url(
                scope="profile",
                response_type="code",
                redirect_uri=self.get_callback_url(),
            )
        )

    def callback(self):
        pass

    def get_callback_url(self):
        return url_for(".oauth_callback", provider=self.provider_name, _external=True)

    @classmethod
    def get_provider(cls, provider_name):
        if cls.providers is None:
            cls.providers = {}
            for provider_class in cls.__subclasses__():
                provider = provider_class()
                cls.providers[provider.provider_name] = provider
        return cls.providers[provider_name]


class VKSignIn(OAuthSignIn):
    def __init__(self):
        super().__init__("vk")
        self.service = OAuth2Service(
            name="vk",
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url="https://oauth.vk.com/authorize",
            access_token_url="https://oauth.vk.com/access_token",
            base_url="",
        )

    def callback(self):
        if "code" not in request.args:
            return None, None
        oauth_session = self.service.get_raw_access_token(
            data={
                "code": request.args["code"],
                "client_id": self.consumer_id,
                "client_secret": self.consumer_secret,
                "redirect_uri": self.get_callback_url(),
            },
        )

        user_id = oauth_session.json().get("user_id")
        token = oauth_session.json().get("access_token")

        return user_id, token


class GoogleSignIn(OAuthSignIn):
    def __init__(self):
        super().__init__("google")
        self.service = OAuth2Service(
            name="google",
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url="https://accounts.google.com/o/oauth2/auth",
            access_token_url="https://accounts.google.com/o/oauth2/token",
            base_url="",
        )

    def callback(self):
        if "code" not in request.args:
            return None, None
        oauth_session = self.service.get_raw_access_token(
            data={
                "code": request.args["code"],
                "grant_type": "authorization_code",
                "redirect_uri": self.get_callback_url(),
            },
        )

        user_id = oauth_session.json().get("id_token")
        token = oauth_session.json().get("access_token")

        return user_id, token


class UserInfoVK:
    def __init__(self, user_id, token):
        self.data = {
            "user_id": user_id,
            "v": "5.131",
            "fields": "photo",
            "access_token": token,
        }
        self.response = requests.get(
            "https://api.vk.com/method/users.get", params=self.data
        )

    def get_avatar(self):
        if self.response.json():
            avatar = self.response.json().get("response")[0]["photo"]
            return avatar
        return None

    def get_firstname_lastname(self):
        if self.response.json():
            user_info = self.response.json().get("response")[0]
            first_name, last_name = user_info["first_name"], user_info["last_name"]
            return first_name, last_name
        return None


class UserInfoGoogle:
    def __init__(self, token):
        self.data = {
            "access_token": token,
        }
        self.response = requests.get(
            "https://www.googleapis.com/oauth2/v1/userinfo?alt=json", params=self.data
        )

    def get_avatar(self):
        if self.response.json():
            avatar = self.response.json()["picture"]
            return avatar
        return None

    def get_firstname_lastname(self):
        if self.response.json():
            user_info = self.response.json()
            first_name, last_name = user_info["given_name"], user_info["family_name"]
            return first_name, last_name
        return None
