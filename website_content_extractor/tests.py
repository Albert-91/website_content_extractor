import unittest

import requests
from django.core.exceptions import ValidationError
from django.test import TestCase
from requests.exceptions import MissingSchema
from website_content_extractor.utils import get_url_photos_from_html


# ValidationError, MissingSchema, requests.HTTPError

# print(get_url_photos_from_website('www.wwww.pl/'))


class GetUrlPhotosFromWebsite(TestCase):

    def test__photo_url_extractor__should__return__None_if_url_has_no_scheme(self):
        self.assertEqual(get_url_photos_from_html('www.google.pl'), None)

    def test__photo_url_extractor__should__return__None_if_scheme_is_invalid(self):
        self.assertEqual(get_url_photos_from_html('htts://www.google.pl'), None)

    def test__photo_url_extractor__should__return__None__if_(self):
        url = "https://github.com/Albert-91/semantive_scrapping_text_and_images_from_url"
        self.assertEqual(get_url_photos_from_html(url), None)

    def test__photo_url_extractor__should__return__None_if_domain_does_not_exist(self):
        self.assertEqual(get_url_photos_from_html('http://www.onetwothree.pl'), None)

    def test__photo_url_extractor__should__return__None_input_is_not_correct_url(self):
        self.assertEqual(get_url_photos_from_html('http://www.onetwothreepl'), None)

    def test__photo_url_extractor__should__return__not_empty_list(self):
        len_of_list = len(get_url_photos_from_html('http://www.google.pl'))
        self.assertGreater(len_of_list, 0)

    def test__photo_url_extractor__should__return__list_with_correct_urls(self):
        photo_urls = get_url_photos_from_html('https://en.wikipedia.org/wiki/Hulk')
        for url in photo_urls:
            self.assertNotEqual(get_url_photos_from_html(url), None)


if __name__ == "__main__":
    unittest.main()
