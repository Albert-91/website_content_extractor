from django.test import TestCase

from website_content_extractor.utils import get_url_images_from_html, get_text_from_html


class GetUrlPhotosFromHtml(TestCase):

    def test__photo_url_extractor__should__return__None_if_url_is_not_string(self):
        self.assertEqual(get_url_images_from_html(2), None)

    def test__photo_url_extractor__should__return__None_if_url_has_no_scheme(self):
        self.assertEqual(get_url_images_from_html('www.google.pl'), None)

    def test__photo_url_extractor__should__return__None_if_scheme_is_invalid(self):
        self.assertEqual(get_url_images_from_html('htts://www.google.pl'), None)

    def test__photo_url_extractor__should__return__None__if_status_code_is_404(self):
        url = "https://github.com/Albert-91/semantive_scrapping_text_and_images_from_url"
        self.assertEqual(get_url_images_from_html(url), None)

    def test__photo_url_extractor__should__return__None_if_domain_does_not_exist(self):
        self.assertEqual(get_url_images_from_html('http://www.onetwothree.pl'), None)

    def test__photo_url_extractor__should__return__None_input_is_not_correct_url(self):
        self.assertEqual(get_url_images_from_html('http://www.onetwothreepl'), None)

    def test__photo_url_extractor__should__return__not_empty_list(self):
        len_of_list = len(get_url_images_from_html('http://www.google.pl'))
        self.assertGreater(len_of_list, 0)

    def test__photo_url_extractor__should__return__list_with_correct_urls(self):
        photo_urls = get_url_images_from_html('https://en.wikipedia.org/wiki/Hulk')
        for url in photo_urls:
            self.assertNotEqual(get_url_images_from_html(url), None)


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
