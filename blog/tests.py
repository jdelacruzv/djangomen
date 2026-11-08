from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test import SimpleTestCase
from django.utils import timezone

from .models import Post
from .richtext import sanitize_rich_text

# Create your tests here.


class RichTextSanitizationTests(SimpleTestCase):
    def test_preserves_formatting_and_removes_unsafe_markup(self):
        cleaned = sanitize_rich_text(
            "<p><strong>Texto</strong><script>alert(1)</script>"
            "<img src=x onerror=alert(1)></p>"
        )

        self.assertIn("<strong>Texto</strong>", cleaned)
        self.assertNotIn("script", cleaned)
        self.assertNotIn("onerror", cleaned)
        self.assertNotIn("alert(1)", cleaned)


class PostSearchTests(TestCase):
    def setUp(self):
        self.author = get_user_model().objects.create_user(username='search-author')

    def create_post(self, title, text, published=True):
        return Post.objects.create(
            author=self.author,
            title=title,
            text=text,
            published_date=timezone.now() if published else None,
        )

    def test_post_list_searches_only_titles(self):
        title_match = self.create_post('Django avanzado', 'Contenido general')
        self.create_post(
            'Otro artículo', '<p>Aprender Django</p>')
        self.create_post('Borrador Django',
                         'No debe aparecer', published=False)

        response = self.client.get('/', {'q': 'django'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            {post.pk for post in response.context['posts']},
            {title_match.pk},
        )
        self.assertEqual(response.context['query'], 'django')

    def test_suggestions_require_two_characters_and_only_include_published_posts(self):
        published = self.create_post('Python para todos', 'Introducción')
        self.create_post('Artículo diferente',
                         'Menciona Python en el contenido')
        self.create_post('Python borrador', 'Privado', published=False)

        short_response = self.client.get('/buscar/sugerencias/', {'q': 'p'})
        response = self.client.get('/buscar/sugerencias/', {'q': 'python'})

        self.assertEqual(short_response.json(), {'results': []})
        self.assertEqual(
            response.json(),
            {'results': [{'title': published.title,
                          'url': f'/post/{published.pk}/'}]},
        )

    def test_suggestions_are_limited_to_five_results(self):
        for index in range(6):
            self.create_post(f'Django {index}', 'Artículo publicado')

        response = self.client.get('/buscar/sugerencias/', {'q': 'django'})

        self.assertEqual(len(response.json()['results']), 5)
