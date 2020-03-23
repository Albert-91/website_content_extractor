import re

from django.test import TestCase

from website_content_extractor.models import QueueTask
from website_content_extractor.utils import get_url_images_from_html, get_text_from_html, validate_url


class GetUrlImagesFromHtml(TestCase):

    def test__image_url_extractor__should__return__None_if_url_is_not_string(self):
        self.assertEqual(get_url_images_from_html(2), None)

    def test__image_url_extractor__should__return__None_if_url_has_no_scheme(self):
        self.assertEqual(get_url_images_from_html('www.google.pl'), None)

    def test__image_url_extractor__should__return__None_if_scheme_is_invalid(self):
        self.assertEqual(get_url_images_from_html('htts://www.google.pl'), None)

    def test__image_url_extractor__should__return__None__if_status_code_is_404(self):
        url = "https://github.com/Albert-91/semantive_scrapping_text_and_images_from_url"
        self.assertEqual(get_url_images_from_html(url), None)

    def test__image_url_extractor__should__return__None_if_domain_does_not_exist(self):
        self.assertEqual(get_url_images_from_html('http://www.onetwothree.pl'), None)

    def test__image_url_extractor__should__return__None_input_is_not_correct_url(self):
        self.assertEqual(get_url_images_from_html('http://www.onetwothreepl'), None)

    def test__image_url_extractor__should__return__not_empty_list(self):
        len_of_list = len(get_url_images_from_html('http://www.google.pl'))
        self.assertGreater(len_of_list, 0)

    def test__image_url_extractor__should__return__list_with_correct_urls(self):
        image_urls = get_url_images_from_html('https://en.wikipedia.org/wiki/Hulk')
        for url in image_urls:
            self.assertNotEqual(validate_url(url), None)


class GetTextFromHtml(TestCase):

    def test__text_extractor__should__return__None_if_url_is_not_string(self):
        self.assertEqual(get_text_from_html(2), None)

    def test__text_extractor__should__return__None_if_url_has_no_scheme(self):
        self.assertEqual(get_text_from_html('www.google.pl'), None)

    def test__text_extractor__should__return__None_if_scheme_is_invalid(self):
        self.assertEqual(get_text_from_html('htts://www.google.pl'), None)

    def test__text_extractor__should__return__None__if_if_status_code_is_404(self):
        url = "https://github.com/Albert-91/semantive_scrapping_text_and_images_from_url"
        self.assertEqual(get_text_from_html(url), None)

    def test__text_extractor__should__return__None_if_domain_does_not_exist(self):
        self.assertEqual(get_text_from_html('http://www.onetwothree.pl'), None)

    def test__text_extractor__should__return__None_input_is_not_correct_url(self):
        self.assertEqual(get_text_from_html('http://www.onetwothreepl'), None)

    def test__text_extractor__should__return__not_empty_list(self):
        len_of_list = len(get_text_from_html('http://www.google.pl'))
        self.assertGreater(len_of_list, 0)


class TestQueueTaskModel(TestCase):

    def test__url_field_regex__should__return__true(self):
        pattern = QueueTask.regex
        test_urls = [
            'www.google.pl',
            'www.google.com',
            'www.google.com/abc',
            'www.google.com/abc.html',
            'www.google.com/abc#def',
            'www.google.com@aaa/abc#def',
            'www.google.com/abc/111#def',
            'http://www.google.pl',
            'http://www.google.com',
            'http://dev.google.com',
            'http://google.com',
            'http://www.google.com/abc',
            'http://www.google.com/abc.html',
            'http://www.google.com/abc#def',
            'http://www.google.com@aaa/abc#def',
            'http://www.google.com/abc/111#def',
            'https://www.google.pl',
            'https://www.google.com',
            'https://dev.google.com',
            'https://google.com',
            'https://www.google.com/abc',
            'https://www.google.com/abc.html',
            'https://www.google.com/abc#def',
            'https://www.google.com@aaa/abc#def',
            'https://www.google.com/abc/111#def',
        ]
        for url in test_urls:
            result = re.match(pattern, url)
            self.assertTrue(result)

    def test__url_field_regex__should__return__false(self):
        pattern = QueueTask.regex
        test_urls = [
            'http//www.google.pl',
            'http:/www.google.pl',
            'sftp://www.google.com',
            'ftp://www.google.com',
            'http:/www.google.paaaal',
            'http:/www.google.pl/@#aa',
            'http:/wwwgoogle.pl',
            'http:/www.googlepl',
            'google.pl',
            'dev.google.com',
        ]
        for url in test_urls:
            result = re.match(pattern, url)
            self.assertFalse(result)
