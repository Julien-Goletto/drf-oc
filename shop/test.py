from rest_framework.test import APITestCase
from django.urls import reverse, reverse_lazy
from rest_framework import status
from unittest import mock

from shop.models import Category, Product, Article
from shop.mocks import ECOSCORE_GRADE, mock_openfoodfact_success

class ShopAPITestCase(APITestCase):
    # Helper function to harmonize time notation accordingly to API
    def format_datetime(self, value):
        return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    
class TestCategory(ShopAPITestCase):
    url = reverse_lazy('category-list')
    
    # data initialization
    def test_category_list(self):
        category = Category.objects.create(name='Fruits', active=True)
        Category.objects.create(name='Légumes')

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': 
                [
                    {
                        'id': category.pk,
                        'name': category.name,
                        'description': category.description,
                        'date_created': self.format_datetime(category.date_created),
                        'date_updated': self.format_datetime(category.date_updated),
                    }
                ],
        }
        self.assertEqual(response.json(), expected)
    
    def test_category_detail(self):
        category = Category.objects.create(name='Fruits', active=True)
        response = self.client.get(reverse('category-detail', kwargs={'pk': category.pk}))
        expected = {
            'id': category.pk,
            'name': category.name,
            'description': category.description,
            'products': [],
            'date_created': self.format_datetime(category.date_created),
            'date_updated': self.format_datetime(category.date_updated),
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected)
        

    def test_create(self):
        # First check no category exists
        self.assertFalse(Category.objects.exists())
        # Create a new one throught a Post request
        response = self.client.post(self.url, data={'name': 'Nouvelle Catégorie'})
        # Creation can't be done from a HTTP request
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertFalse(Category.objects.exists())

class TestProduct(ShopAPITestCase):
    url = reverse_lazy('product-list')

    @mock.patch('shop.models.Product.call_external_api', mock_openfoodfact_success)
    def test_product_list_and_details(self):
        category = Category.objects.create(name='Fruits', active=True)
        product = Product.objects.create(name='Abricot', description='Juteux et gorgé de soleil', active=True, category_id=category.id)
        Product.objects.create(name='Orange', description='Juteuse et gorgée de soleil', active=False, category_id=category.id)

        self.assertEqual(self.client.get(self.url).status_code, status.HTTP_200_OK)

        expected_details = {
                        'id': product.id,
                        'name': product.name,
                        'description': product.description,
                        'ecoscore': ECOSCORE_GRADE,
                        'category_id': product.category_id,
                        'articles': [],
                        'date_created': self.format_datetime(product.date_created),
                        'date_updated': self.format_datetime(product.date_updated),
        }

        general_details = expected_details.copy()
        for key in ['description', 'category_id', 'articles']:
            del general_details[key]

        expected_list = {
            'count': 1,
            'next': None,
            'previous': None,
            'results':
                [
                    general_details,
                ]
        }
        
        list_response = self.client.get(self.url)
        self.assertEqual(list_response.json(), expected_list)
        details_response = self.client.get(self.url + f'{product.id}/')
        self.assertEqual(details_response.status_code, status.HTTP_200_OK)
        self.assertEqual(details_response.data, expected_details)
    
    def test_impossible_to_mutate_through_http_request(self):
        # Post test
        self.assertFalse(Product.objects.exists())
        post_response = self.client.post(self.url, data={'name':'Abricot'})
        self.assertEqual(post_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertFalse(Product.objects.exists())

        # Put and delete test
        category = Category.objects.create(name='Fruits', active=True)
        product = Product.objects.create(name='Abricot', description='Juteux et gorgé de soleil', active=True, category_id=category.id)

        put_response = self.client.put(self.url + f'{product.id}/', data={'name': 'Tomate'})
        self.assertEqual(put_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertContains(self.client.get(self.url  + f'{product.id}/'), 'Abricot', count=1, status_code=status.HTTP_200_OK)

        delete_response = self.client.delete(self.url + f'{product.id}/')
        self.assertEqual(delete_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEquals(self.client.get(self.url  + f'{product.id}/').status_code, status.HTTP_200_OK)

