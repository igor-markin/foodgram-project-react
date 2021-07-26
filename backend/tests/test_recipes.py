import pytest
from rest_framework import status


class TestTag:
    @pytest.mark.django_db(transaction=True)
    @pytest.mark.parametrize('url', ['/api/tags/', '/api/tags/{id}/'])
    def test_get_tags(self, api_client, tag, url):
        r = api_client.get(url.format(id=tag.pk))
        assert r.status_code == status.HTTP_200_OK


class TestIngredient:
    @pytest.mark.django_db(transaction=True)
    @pytest.mark.parametrize('url', [
        '/api/ingredients/',
        '/api/ingredients/{id}/',
        '/api/ingredients/?name={name}'
    ])
    def test_get_ingredients(self, api_client, ingredient, url):
        r = api_client.get(url.format(id=ingredient.pk, name=ingredient.name))
        assert r.status_code == status.HTTP_200_OK


class TestFavorite:
    @pytest.mark.django_db(transaction=True)
    def test_favorite_with_unauth_user(self, api_client, recipe):
        r = api_client.get(f'/api/recipes/{recipe.pk}/favorite/')
        assert r.status_code == status.HTTP_401_UNAUTHORIZED

        r = api_client.delete(f'/api/recipes/{recipe.pk}/favorite/')
        assert r.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db(transaction=True)
    def test_favorite_with_auth_user(self, api_user_client, recipe):
        r = api_user_client.get(f'/api/recipes/{recipe.pk}/favorite/')
        assert r.status_code == status.HTTP_201_CREATED

        r = api_user_client.get(f'/api/recipes/{recipe.pk}/favorite/')
        assert r.status_code == status.HTTP_400_BAD_REQUEST

        r = api_user_client.delete(f'/api/recipes/{recipe.pk}/favorite/')
        assert r.status_code == status.HTTP_204_NO_CONTENT

        r = api_user_client.delete(f'/api/recipes/{recipe.pk}/favorite/')
        assert r.status_code == status.HTTP_404_NOT_FOUND


class TestShoppingCart:
    @pytest.mark.django_db(transaction=True)
    def test_download_shopping_cart_with_unauth_user(self, client):
        r = client.get('/api/recipes/download_shopping_cart/')
        assert r.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db(transaction=True)
    def test_download_shopping_cart_with_auth_user(self, api_user_client):
        r = api_user_client.get('/api/recipes/download_shopping_cart/')
        assert r.status_code == status.HTTP_200_OK

    @pytest.mark.django_db(transaction=True)
    def test_shopping_cart_with_unauth_user(self, client):
        r = client.get('/api/recipes/999/shopping_cart/')
        assert r.status_code == status.HTTP_401_UNAUTHORIZED

        r = client.delete('/api/recipes/999/shopping_cart/')
        assert r.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db(transaction=True)
    def test_shopping_cart_with_auth_user(self, api_user_client, recipe):
        r = api_user_client.get(f'/api/recipes/{recipe.pk}/shopping_cart/')
        assert r.status_code == status.HTTP_201_CREATED

        r = api_user_client.get(f'/api/recipes/{recipe.pk}/shopping_cart/')
        assert r.status_code == status.HTTP_400_BAD_REQUEST

        r = api_user_client.delete(f'/api/recipes/{recipe.pk}/shopping_cart/')
        assert r.status_code == status.HTTP_204_NO_CONTENT

        r = api_user_client.delete(f'/api/recipes/{recipe.pk}/shopping_cart/')
        assert r.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.django_db(transaction=True)
    def test_get_recipe_list(self, client):
        r = client.get('/api/recipes/')
        assert r.status_code == status.HTTP_200_OK


class TestRecipe:
    @pytest.mark.django_db(transaction=True)
    def test_create_recipe_with_unauth_user(self, client):
        r = client.post('/api/recipes/')
        assert r.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db(transaction=True)
    def test_create_recipe_with_auth_user(self, api_user_client, ingredient, tag):
        data = {
            "tags": [tag.pk],
            "name": "test",
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAA"
                     "BieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw"
                     "4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
            "text": "test",
            "cooking_time": 1,
            "ingredients": [
                {"id": ingredient.pk, "amount": 10}
            ]
        }

        r = api_user_client.post('/api/recipes/', data=data)
        assert r.status_code == status.HTTP_201_CREATED

        r = api_user_client.post('/api/recipes/', data=data)
        assert r.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.django_db(transaction=True)
    def test_get_recipe(self, api_client, recipe):
        r = api_client.get(f'/api/recipes/{recipe.pk}/')
        assert r.status_code == status.HTTP_200_OK

        r = api_client.get('/api/recipes/999/')
        assert r.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.django_db(transaction=True)
    def test_put_recipe_with_unauth_user(self, client):
        r = client.put('/api/recipes/999/')
        assert r.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.django_db(transaction=True)
    def test_put_recipe_with_auth_user(self, api_user_client, recipe,
                                       ingredient, tag, tag_2, user):
        data = {
            'ingredients': [
                {"id": ingredient.pk, "amount": 111}
            ],
            'tags': [tag.pk, tag_2.pk],
            'author': user,
            'name': 'Банан в шоколаде',
            'image': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAA'
                     'BieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw'
                     '4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==',
            'text': 'Непревзойдённый вкус мягкого банана и теплого шоколада',
            'cooking_time': 120
        }
        r = api_user_client.put(f'/api/recipes/{recipe.pk}/', data=data)
        assert r.status_code == status.HTTP_200_OK

        data = {'cooking_time': -90}
        r = api_user_client.put(f'/api/recipes/{recipe.pk}/', data=data)
        assert r.status_code == status.HTTP_400_BAD_REQUEST

        data = {'name': 'Банан в шоколадном масле', 'cooking_time': 90}
        r = api_user_client.put('/api/recipes/999/', data=data)
        assert r.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.django_db(transaction=True)
    def test_delete_recipe_with_unauth_user(self, client):
        r = client.delete('/api/recipes/999/')
        assert r.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.django_db(transaction=True)
    def test_delete_recipe_with_author(self, api_user_client, recipe):
        """ Пока не полез в lazy-fixture, голова кипит """
        r = api_user_client.delete(f'/api/recipes/{recipe.pk}/')
        assert r.status_code == status.HTTP_204_NO_CONTENT

        r = api_user_client.delete(f'/api/recipes/{recipe.pk}/')
        assert r.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.django_db(transaction=True)
    def test_delete_recipe_with_non_author(self, api_user_client_2, recipe):
        r = api_user_client_2.delete(f'/api/recipes/{recipe.pk}/')
        assert r.status_code == status.HTTP_403_FORBIDDEN
