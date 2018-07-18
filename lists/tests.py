from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

import re

from lists.views import home_page

# Create your tests here.

def remove_csrf(html_code):
    # csrf_regex = r'&lt;input[^&gt;]+csrfmiddlewaretoken[^&gt;]+&gt;'
    csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
    return re.sub(csrf_regex, '', html_code)


class HomePageTest(TestCase):

    def test_home_page_is_about_todo_lists(self):
        request = HttpRequest()

        response = home_page(request)

        #this method stopped working as soon as our template contained tags like csrf_token
        #with open('lists/templates/home.html') as f:
        #    expected_content = f.read()
        #self.assertEqual(response.content.decode(), expected_content)

        expected_content = render_to_string('home.html', request=request)
        self.assertEqual(remove_csrf(response.content.decode()), remove_csrf(expected_content))

    def test_home_page_can_remember_post_requests(self):
        request = HttpRequest()
        request.method = "POST"
        request.POST['item_text'] = "A new item"

        response = home_page(request)

        self.assertIn("A new item", response.content.decode())

        expected_content = render_to_string('home.html', {'new_item_text': 'A new item'})
        self.assertEqual(remove_csrf(response.content.decode()), remove_csrf(expected_content))