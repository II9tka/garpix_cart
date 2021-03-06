from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient

from ..models import CartItem


class CartViewTestCase(TestCase):
    def setUp(self):
        User = get_user_model()
        self.username = 'testuser1'
        self.password = '12345'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user.save()
        client = APIClient()
        client.force_authenticate(user=self.user)
        self.client = client

    def test_add(self):
        response = self.client.post(
            '/api/v1/cart/add/',
            {
                'data': [
                    {
                        'product': 1,
                        'count': 1,
                        'params': {
                            'color': '#000000'
                        }
                    }
                ]
            },
            format='json',
            HTTP_ACCEPT='application/json'
        )

        self.assertEqual(response.status_code, 200)
        count = CartItem.objects.all().count()
        self.assertEqual(count, 1)

    def test_remove(self):
        cart_item = CartItem(
            product=1,
            count=1,
            params=dict(),
            user=self.user
        )
        cart_item.save()

        response = self.client.delete(
            '/api/v1/cart/remove/',
            {
                'data': [
                    cart_item.pk
                ]
            },
            format='json',
            HTTP_ACCEPT='application/json'
        )

        self.assertEqual(response.status_code, 200)

        count = CartItem.objects.all().count()
        self.assertEqual(count, 0)

    def test_update(self):
        product_count = 2
        cart_item = CartItem(
            product=1,
            count=1,
            params=dict(),
            user=self.user
        )
        cart_item.save()

        response = self.client.patch(
            f'/api/v1/cart/{cart_item}/',
            {
                'data': {
                    'count': product_count
                }
            },
            format='json',
            HTTP_ACCEPT='application/json'
        )

        self.assertEqual(response.status_code, 200)

        obj = CartItem.objects.get(pk=cart_item.pk)
        self.assertEqual(obj.count, product_count)
