import logging
from typing import Text, List, Union
from urllib.parse import urlparse, urlunparse

import bs4 as bs
import requests
from bs4.element import Comment
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from requests import Response
from requests.exceptions import MissingSchema, ConnectionError, HTTPError, InvalidSchema

logger = logging.getLogger(__name__)


def get_url_images_from_html(url: Text) -> Union[List[Text], None]:
    """
    Function gets url and returns a list of urls with all images from url input
    :param url:
    :return: list of urls with images
    """

    r = validate_url(url)
    if r:
        parsed_url = urlparse(url)
        soup = bs.BeautifulSoup(r.text, features='html.parser')
        url_images = []
        for img_tag in soup.find_all('img'):
            url_photo = img_tag.attrs.get('src') or img_tag.attrs.get('data-src')
            if not url_photo:
                continue
            parsed_url_photo = urlparse(url_photo)
            if not parsed_url_photo.scheme or not parsed_url_photo.netloc:
                url_photo = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url_photo.path, None, None, None))
            if validate_url(url_photo):
                url_images.append(url_photo)
        return url_images


def get_text_from_html(url: Text) -> Union[List[Text], None]:
    r = validate_url(url)
    if r:
        soup = bs.BeautifulSoup(r.text, 'html.parser')
        texts = soup.findAll(text=True)
        visible_texts = filter(_get_visible_tag, texts)
        visible_texts = [text.replace('\n', ' ').replace('\r', '').strip() for text in visible_texts]
        visible_texts = [" ".join(text.split()) for text in visible_texts if text != '']
        return visible_texts


def validate_url(url: Text) -> Union[Response, None]:
    r = None
    try:
        URLValidator(url)
        r = requests.get(url=url)
        if not r.status_code == 200:
            raise HTTPError(f"Request status code is {r.status_code} but should 200.")
    except (ValidationError, MissingSchema, HTTPError, ConnectionError, InvalidSchema) as e:
        logger.error(e)
    return r


def _get_visible_tag(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True
