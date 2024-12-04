from django.test import TestCase
from customs.models import Customers,Order
from rest_framework.test import APIClient
from unittest.mock import patch,Mock


class APITestCase(TestCase):

    def setUp(self):

        self.client=APIClient()

        self.customer= Customers.objects.create(
            name='test customer',
            email='testcustomer@gmail.com',
            phone_number='+254712345678',
            code=12345
        )

        self.order_data={
            "customer": self.customer.id,
            "Items": "test_item1,test_item2",
            "amount":"25000.80"
        }
    
    def tearDown(self):
        Customers.objects.all().delete()
        Order.objects.all().delete()


    def test_create_order(self):
        response = self.client.post('/customs/orders/new/', self.order_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('message', response.data)  
        self.assertTrue(Order.objects.filter(customer=self.customer).exists())  

    def test_create_customer(self):
        customer_data = {
            "name": "New Customer",
            "email": "newcustomer@example.com",
            "phone_number": "+254798765432",
        }
        response = self.client.post('/customs/customers/new/', customer_data, format='json')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Customers.objects.filter(email="newcustomer@example.com").exists())
        
    @patch('customs.views.requests.post')  
    @patch('customs.views.requests.get')  
    def test_google_auth(self, mock_get, mock_post):
     mock_post_response = Mock()
     mock_post_response.json.return_value = {
        "access_token": "fake_access_token", 
        "email": "testoauth@example.com", 
        "name": "OAuth User"
    }
     mock_post_response.status_code = 200
     mock_post.return_value = mock_post_response

     mock_get_response = Mock()
     mock_get_response.json.return_value = {"email": "testoauth@example.com"}  # Mock email
     mock_get.return_value = mock_get_response

     response = self.client.get('/customs/customers/google/callback/', {"token": "fake_token"}, format='json')

     self.assertEqual(response.status_code, 200)

     self.assertTrue(Customers.objects.filter(email="testoauth@example.com").exists(), 
                    "Customer with the email 'testoauth@example.com' was not created.")


    def test_get_orders(self):
        Order.objects.create(customer=self.customer, Items="Item A, Item B", amount="50.00")
        response = self.client.get(f'/customs/orders/{self.customer.id}/')

        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)  

    def test_get_customer(self):
        response = self.client.get(f'/customs/customers/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['email'], self.customer.email)

