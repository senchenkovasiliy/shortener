import requests
import re
from fastapi import status


def is_valid_url(url: str) -> bool:
    """
    Boolean flag as a validator
    Validator for urls send from user
    """
    if not url:
        return False

    regex = ("((http|https)://)(www.)?" +
             "[a-zA-Z0-9@:%._\\+~#?&//=]" +
             "{2,256}\\.[a-z]" +
             "{2,6}\\b([-a-zA-Z0-9@:%" +
             "._\\+~#?&//=]*)")
    p = re.compile(regex)
    return True if re.search(p, url) else False


def validate_url(url: str) -> None:
    """
    Validations urls
    """
    if not is_valid_url(url):
        raise ValueError(f"Validation Error. Provided url '{url}' is not valid.")
    try:
        response = requests.get(url)
    except Exception as e:
        raise ValueError(f"Validation Error. '{url}' website doesn't exists.")
    else:
        if response.status_code != status.HTTP_200_OK:
            raise ValueError(f"Validation Error. '{url}' website doesn't exists.")
