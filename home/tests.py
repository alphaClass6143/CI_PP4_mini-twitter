from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from home.models import CustomUser
from django.urls import reverse

class ViewTestCase(TestCase):
    def test_home_view_with_offset(self):
        # Create some test data
        for i in range(20):
            Post.objects.create(title=f'Post {i}', body='Test body')

        # Send a GET request to the home view with an offset of 10
        response = self.client.get(reverse('home'), {'offset': 10})
        self.assertEqual(response.status_code, 200)

        # Check that the correct template is being used
        self.assertTemplateUsed(response, 'home/index.html')

        # Check that the correct context variables are being passed to the template
        self.assertIn('post_list', response.context)
        self.assertEqual(len(response.context['post_list']), 10)
        self.assertEqual(response.context['post_list'][0].title, 'Post 9')
        self.assertIn('form', response.context)

