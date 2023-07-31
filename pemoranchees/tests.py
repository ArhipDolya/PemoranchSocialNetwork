from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from .models import Pemoran


User = get_user_model()

class PemoranTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='Arhip', password='password1234')
        Pemoran.objects.create(content='new 1 pemoran', user=self.user) 
        
    def test_pemoran_exists(self):
        pemoran = Pemoran.objects.create(content='new 2 pemoran', user=self.user)
        self.assertEqual(pemoran.id, 2)
        self.assertEqual(pemoran.user, self.user)

    def get_client(self):
        client = APIClient()
        client.login(username=self.user.username, password='password1234')

        return client

    def test_pemoranch_items(self):
        client = self.get_client()
        responce = client.get('/api/pemos/')
        self.assertEqual(responce.status_code, 200)
        self.assertEqual(len(responce.json()), 1)

    def test_pemoranch_action_like(self):
        client = self.get_client()
        responce = client.post('/api/pemos/action/', {'id': 1, 'action': 'like'})
        self.assertEqual(responce.status_code, 200)
        likes = responce.json().get('likes')
        self.assertEqual(likes, 1)
    
    def test_pemoranch_action_unlike(self):
        client = self.get_client()
        responce = client.post('/api/pemos/action/', {'id': 1, 'action': 'like'})
        self.assertEqual(responce.status_code, 200)
        responce = client.post('/api/pemos/action/', {'id': 1, 'action': 'unlike'})
        self.assertEqual(responce.status_code, 200)
        likes = responce.json().get('likes')
        self.assertEqual(likes, 0)

    def test_pemoranch_action_repemo(self):
       client = self.get_client()
       responce = client.post('/api/pemos/action/', {'id': 1, 'action': 'repemo'})
       self.assertEqual(responce.status_code, 200)

    def test_pemoranch_create_view(self):
        client = self.get_client()
        data = {'content': 'New pemo'}

        responce = client.post('api/pemos/create/', data=data)
        self.assertEqual(responce.status_code, 404)

    def test_pemoranch_detail_view(self):
        client = self.get_client()
        responce = client.get('/api/pemos/1/')
        self.assertEqual(responce.status_code, 200)
        data = responce.json()
        _id = data.get('id')
        self.assertEqual(_id, 1)

    def test_pemoranch_detail_view(self):
        client = self.get_client()
        responce = client.delete('/api/pemos/1/delete/')
        self.assertEqual(responce.status_code, 204)

        client = self.get_client()
        responce = client.delete('/api/pemos/1/delete/')
        self.assertEqual(responce.status_code, 404)