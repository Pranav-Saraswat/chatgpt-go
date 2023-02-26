import json
import uuid
from os import environ
from os import getenv
from os.path import exists

import requests

from OpenAIAuth import Authenticator, Error as AuthError

def configure():
    """
    Looks for a config file in the following locations:
    """
    config_files = ["config.json"]
    if xdg_config_home := getenv("XDG_CONFIG_HOME"):
        config_files.append(f"{xdg_config_home}/revChatGPT/config.json")
    if user_home := getenv("HOME"):
        config_files.append(f"{user_home}/.config/revChatGPT/config.json")

    if config_file := next((f for f in config_files if exists(f)), None):
        with open(config_file, encoding="utf-8") as f:
            config = json.load(f)
    else:
        print("No config file found.")
        raise Exception("No config file found.")
    return config
    
def main(config: dict):
    """
    Main function for the chatGPT program.
    """
    print("Logging in...")

    if (
        "email" not in config or "password" not in config
    ) and "session_token" not in config:
        raise Exception("No login details provided!")

    auth = Authenticator(
        email_address=config.get("email"),
        password=config.get("password"),
        proxy=config.get("proxy"),
    )

    auth.begin()
    print("Logging success")

    session_token = auth.session_token
    print(f"session token:{session_token}")

    access_token = auth.get_access_token()
    print(f"access token:{access_token}")


if __name__ == "__main__":
    main(configure())