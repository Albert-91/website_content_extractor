import logging
from typing import Text, List, Union
from urllib.parse import urlparse

import bs4 as bs
import requests
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from requests import Response
from requests.exceptions import MissingSchema, ConnectionError, HTTPError

logger = logging.getLogger(__name__)


def get_url_photos_from_website(url: Text) -> Union[List[Text], None]:
    """
    Function gets url and returns a list of urls with all images from url input
    :param url:
    :return: list of urls with images
    """

    r = validate_url(url)
    parsed_uri = urlparse(url)

    if r:
        soup = bs.BeautifulSoup(r.text, features='html.parser')
        url_photos = []
        for img_tag in soup.find_all('img'):
            url_photo = img_tag['src']
            p = urlparse(url_photo)
            if not p.hostname:
                url_photo = parsed_uri.hostname + url_photo
            if not p.scheme:
                url_photo = parsed_uri.scheme + ':' + url_photo if url_photo.startswith('//') else parsed_uri.scheme + '://' + url_photo
            if validate_url(url_photo):
                url_photos.append(url_photo)
        return url_photos


def validate_url(url: Text) -> Union[Response, None]:
    r = None
    try:
        URLValidator(url)
        r = requests.get(url=url)
        if not r.status_code == 200:
            raise HTTPError("Request status code is not equal 200.")
    except (ValidationError, MissingSchema, HTTPError, ConnectionError) as e:
        logger.error(e)
    return r
