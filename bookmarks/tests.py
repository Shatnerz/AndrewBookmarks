from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

class RegisterTest(TestCase):
    """Test registering users"""
    
    def setUp(self):
        self.client = Client()
        
    def test_register_page(self):
        data = {
            'username': 'user',
            'email': 'user@test.com',
            'password1': 'Testing',
            'password2': 'Testing'
        }
        response = self.client.post('/bookmarks/register/', data)
        self.assertEqual(response.status_code, 302)
        
    def test_register_page_incorrect_pw(self):
        data = {
            'username': 'user',
            'email': 'user@test.com',
            'password1': 'one',
            'password2': 'two'
        }
        response = self.client.post('/bookmarks/register/', data)
        self.assertEqual(response.status_code, 200)
        
class BookmarkTest(TestCase):
    """Test to make sure bookmarks save correctly"""
    
    def setUp(self):
        self.client = Client()
        user = User.objects.create_user('username', 'user@test.com', 'pw')
        user.save()
        
    def test_bookmark_save(self):
        self.client.login(
            username='username',
            password='pw',
        )
        data = {
            'url': 'http://www.test.com/',
            'title': 'Test URL',
            'description': 'Test description'
        }
        response = self.client.post('/bookmarks/save/', data)
        response = self.client.get('/bookmarks/user/username/')
        #print response.content
        self.assertTrue('http://www.test.com/' in response.content)
        self.assertTrue('Test URL' in response.content)
        self.assertTrue('Test description' in response.content)
