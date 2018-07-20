from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

import re

from lists.views import home_page
from lists.models import Item

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


class NewListViewTest(TestCase):

    def test_can_save_post_requests_to_database(self):
        response = self.client.post('/lists/new', {'item_text': 'A new item'})

        item_from_db = Item.objects.all()[0]
        self.assertEqual(item_from_db.text, 'A new item')

    def test_can_save_post_requests_to_database(self):
        response = self.client.post('/lists/new', {'item_text': 'A new item'})
        self.assertEqual(response.status_code, 302)     # Checks for a redirect
        self.assertRedirects(response, '/lists/the-only-list-in-the-world/')


class ListViewTest(TestCase):

    def test_lists_page_shows_items_in_database(self):
        Item.objects.create(text='item 1')
        Item.objects.create(text='item 2')

        response = self.client.get('/lists/the-only-list-in-the-world/')

        self.assertIn('item 1', response.content.decode())
        self.assertContains(response, 'item 2')


from lists.models import Item

class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items_to_the_database(self):
        first_item = Item()
        first_item.text = 'Item the first'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        first_item_from_db = Item.objects.all()[0]
        self.assertEqual(first_item_from_db.text, 'Item the first')

        first_item_from_db = Item.objects.all()[1]
        self.assertEqual(first_item_from_db.text, 'Item the second')

