from flask import Blueprint
from dotenv import load_dotenv
import os


auth = Blueprint("auth", __name__)


dotenv_path = os.path.join("/", ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


def init_config(app):
    app.config["OAUTH_CREDENTIALS"] = {
        "vk": {
            "id": os.getenv("SOCIAL_AUTH_VK_OAUTH2_KEY"),
            "secret": os.getenv("SOCIAL_AUTH_VK_OAUTH2_SECRET"),
        },
        "google": {
            "id": os.getenv("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY"),
            "secret": os.getenv("SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET"),
        },
    }
