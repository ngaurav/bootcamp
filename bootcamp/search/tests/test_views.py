from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from bootcamp.articles.models import Article


class TestViews(TestCase):
    """
    Includes tests for all the functionality
    associated with Views
    """
    def setUp(self):
        self.client = Client()
        self.other_client = Client()
        self.user = get_user_model().objects.create_user(
            username='test_user',
            email='test@gmail.com',
            password='top_secret'
        )
        self.other_user = get_user_model().objects.create_user(
            username='other_test_user',
            email='other_test@gmail.com',
            password='top_secret'
        )
        self.client.login(username='test_user', password='top_secret')
        self.other_client.login(
            username='other_test_user', password='top_secret')
        self.title = 'A really nice to-be title'
        self.content = '''This is a really good content, just if somebody
        published it, that would be awesome, but no, nobody wants to publish
        it, because they know this is just a test, and you know than nobody
        wants to publish a test, just a test; everybody always wants the real
        deal.'''
        self.article = Article.objects.create(
            create_user=self.user, title='A really nice title',
            content=self.content, tags='list, lists', status='P')
        self.article_2 = Article.objects.create(create_user=self.other_user,
                                                title='A bad title',
                                                content="Bad content",
                                                tags='bad', status='P')

    def test_autocomplete_article_suggestions(self):
        search_term = "title"
        question_search_response = self.client.get(
            '/autocomplete/?term='+search_term,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        question_search_suggestions_dict = question_search_response.json()
        self.assertEqual(
            question_search_suggestions_dict[0]['value'], "A bad title")

    def test_autocomplete_user_suggestions(self):
        search_term = "other"
        question_search_response = self.client.get(
            '/autocomplete/?term='+search_term,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        question_search_suggestions_dict = question_search_response.json()
        self.assertEqual(
            question_search_suggestions_dict[0]['value'], "other_test_user")
