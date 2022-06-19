from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
PROFILE_URL = reverse('user:profile')


def create_user(**params):
    # Helper func to create sample users for the test
    return get_user_model().objects.create_user(**params)


class PublicUserAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_valid_user_success(self):
        payload = {'email': 'test@mail.com', 'password': 'testpass', 'name': 'Test'}

        # make the request and test if the user is created or not 
        res = self.client.post(CREATE_USER_URL, payload)
        # self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # # test if the object is actually created
        # user = get_user_model().objects.get(**res.data)

        # self.assertTrue(user.check_password(payload['password']))
        # self.assertNotIn('password', res.data)
        
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)
    
    def test_user_exists(self):
        payload = {
            'email': 'test@mail.com',
            'password': 'testpass',
        }

        create_user(**payload)
        
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        # test password must be greater than 5 characters length
        payload = {
            'email': 'test@mail.com',
            'password': 'pass'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
        # check if user exists
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()

        self.assertFalse(user_exists)
    
    def test_create_token_for_user(self):
        payload = {'email': 'test@test.com', 'password': 'testpass'}
        create_user(**payload)
        
        res = self.client.post(TOKEN_URL, payload)
        
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        create_user(email='test@test.com', password="testpass")
        payload = {'email': 'test@test.com', 'password': 'wrong'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_token_no_user(self):
        """Test that token is not created if user doesn't exist"""
        payload = {'email': 'test@test.com', 'password': 'testpass'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_retrieve_user_unauthorized(self):
        """Test that authentication is required for users"""
        res = self.client.get(PROFILE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication"""

    def setUp(self):
        self.user = create_user(
            email='test@mail.com',
            password='testpass',
            name='name'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in used"""
        res = self.client.get(PROFILE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email
        })

    def test_post_profile_not_allowed(self):
        """Test that POST is not allowed on the profile url"""
        res = self.client.post(PROFILE_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for authenticated user"""
        payload = {'name': 'new name', 'password': 'newpassword123'}

        res = self.client.patch(PROFILE_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
