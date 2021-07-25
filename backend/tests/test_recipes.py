import pytest


@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize('url', ['/api/tags/', '/api/tags/{id}/'])
def test_get_tags(api_client, tag, url):
    r = api_client.get(url.format(id=tag.pk))
    assert r.status_code == 200


@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize('url', [
    '/api/ingredients/',
    '/api/ingredients/{id}/',
    '/api/ingredients/?name={name}'
])
def test_get_ingredients(api_client, ingredient, url):
    r = api_client.get(url.format(id=ingredient.pk, name=ingredient.name))
    assert r.status_code == 200


@pytest.mark.django_db(transaction=True)
def test_favorite_with_unauth_user(api_client, recipe):
    r = api_client.get(f'/api/recipes/{recipe.pk}/favorite/')
    assert r.status_code == 401

    r = api_client.delete(f'/api/recipes/{recipe.pk}/favorite/')
    assert r.status_code == 401


@pytest.mark.django_db(transaction=True)
def test_favorite_with_auth_user(api_user_client, recipe):
    r = api_user_client.get(f'/api/recipes/{recipe.pk}/favorite/')
    assert r.status_code == 201

    r = api_user_client.get(f'/api/recipes/{recipe.pk}/favorite/')
    assert r.status_code == 400

    r = api_user_client.delete(f'/api/recipes/{recipe.pk}/favorite/')
    assert r.status_code == 204

    r = api_user_client.delete(f'/api/recipes/{recipe.pk}/favorite/')
    assert r.status_code == 404


@pytest.mark.django_db(transaction=True)
def test_download_shopping_cart_with_unauth_user(client):
    r = client.get('/api/recipes/download_shopping_cart/')
    assert r.status_code == 401


@pytest.mark.django_db(transaction=True)
def test_download_shopping_cart_with_auth_user(api_user_client):
    r = api_user_client.get('/api/recipes/download_shopping_cart/')
    assert r.status_code == 200


@pytest.mark.django_db(transaction=True)
def test_shopping_cart_with_unauth_user(client):
    r = client.get('/api/recipes/999/shopping_cart/')
    assert r.status_code == 401

    r = client.delete('/api/recipes/999/shopping_cart/')
    assert r.status_code == 401


@pytest.mark.django_db(transaction=True)
def test_shopping_cart_with_auth_user(api_user_client, recipe):
    r = api_user_client.get(f'/api/recipes/{recipe.pk}/shopping_cart/')
    assert r.status_code == 201

    r = api_user_client.get(f'/api/recipes/{recipe.pk}/shopping_cart/')
    assert r.status_code == 400

    r = api_user_client.delete(f'/api/recipes/{recipe.pk}/shopping_cart/')
    assert r.status_code == 204

    r = api_user_client.delete(f'/api/recipes/{recipe.pk}/shopping_cart/')
    assert r.status_code == 404


@pytest.mark.django_db(transaction=True)
def test_get_recipe_list(client):
    r = client.get('/api/recipes/')
    assert r.status_code == 200


@pytest.mark.django_db(transaction=True)
def test_create_recipe_with_unauth_user(client):
    r = client.post('/api/recipes/')
    assert r.status_code == 401


@pytest.mark.django_db(transaction=True)
def test_create_recipe_with_auth_user(api_user_client, ingredient, tag):
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
    assert r.status_code == 201

    r = api_user_client.post('/api/recipes/', data=data)
    assert r.status_code == 400


@pytest.mark.django_db(transaction=True)
def test_get_recipe(api_client, recipe):
    r = api_client.get(f'/api/recipes/{recipe.pk}/')
    assert r.status_code == 200

    r = api_client.get('/api/recipes/999/')
    assert r.status_code == 404


@pytest.mark.django_db(transaction=True)
def test_put_recipe_with_unauth_user(client):
    r = client.put('/api/recipes/999/')
    assert r.status_code == 404


@pytest.mark.django_db(transaction=True)
def test_put_recipe_with_auth_user(api_user_client, recipe,
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
    assert r.status_code == 200

    data = {'cooking_time': -90}
    r = api_user_client.put(f'/api/recipes/{recipe.pk}/', data=data)
    assert r.status_code == 400

    data = {'name': 'Банан в шоколадном масле', 'cooking_time': 90}
    r = api_user_client.put('/api/recipes/999/', data=data)
    assert r.status_code == 404


@pytest.mark.django_db(transaction=True)
def test_delete_recipe_with_unauth_user(client):
    r = client.delete('/api/recipes/999/')
    assert r.status_code == 404


@pytest.mark.django_db(transaction=True)
def test_delete_recipe_with_auth_user(api_user_client, recipe):
    r = api_user_client.delete(f'/api/recipes/{recipe.pk}/')
    assert r.status_code == 204

    r = api_user_client.delete(f'/api/recipes/{recipe.pk}/')
    assert r.status_code == 404
