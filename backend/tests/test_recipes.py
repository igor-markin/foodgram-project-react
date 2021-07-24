import pytest


@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize('url', [['/api/tags/'], ['/api/tags/1']])
def test_get_tags(client, url):
    r = client.get(url)
    assert r.status_code == 200


@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize('url', [
    ['/api/ingredients/'],
    ['/api/ingredients/1'],
    ['/api/ingredients/?name=banana']
])
def test_get_ingredients(client, url):
    r = client.get(url)
    assert r.status_code == 200


@pytest.mark.django_db(transaction=True)
def test_favorite_with_unauth_user(client, recipe):
    r = client.get(f'/api/recipes/{recipe.pk}/favorite/')
    assert r.status_code == 401

    r = client.delete(f'/api/recipes/{recipe.pk}/favorite/')
    assert r.status_code == 401


@pytest.mark.django_db(transaction=True)
def test_favorite_with_auth_user(auth_client, recipe):
    r = auth_client.get(f'/api/recipes/{recipe.pk}/favorite/')
    assert r.status_code == 201

    r = auth_client.get(f'/api/recipes/{recipe.pk}/favorite/')
    assert r.status_code == 400

    r = auth_client.delete(f'/api/recipes/{recipe.pk}/favorite/')
    assert r.status_code == 204

    r = auth_client.delete(f'/api/recipes/{recipe.pk}/favorite/')
    assert r.status_code == 400


@pytest.mark.django_db(transaction=True)
def test_download_shopping_cart_with_unauth_user(client):
    r = client.get('/api/recipes/download_shopping_cart/')
    assert r.status_code == 401


@pytest.mark.django_db(transaction=True)
def test_download_shopping_cart_with_auth_user(auth_client):
    r = auth_client.get('/api/recipes/download_shopping_cart/')
    assert r.status_code == 200


@pytest.mark.django_db(transaction=True)
def test_shopping_cart_with_unauth_user(client):
    r = client.get('/api/recipes/999/shopping_cart/')
    assert r.status_code == 401

    r = client.delete('/api/recipes/999/shopping_cart/')
    assert r.status_code == 401


@pytest.mark.django_db(transaction=True)
def test_shopping_cart_with_auth_user(auth_client, recipe):
    r = auth_client.get(f'/api/recipes/{recipe.pk}/shopping_cart/')
    assert r.status_code == 201

    r = auth_client.get(f'/api/recipes/{recipe.pk}/shopping_cart/')
    assert r.status_code == 400

    r = auth_client.delete(f'/api/recipes/{recipe.pk}/shopping_cart/')
    assert r.status_code == 204

    r = auth_client.delete(f'/api/recipes/{recipe.pk}/shopping_cart/')
    assert r.status_code == 400


@pytest.mark.django_db(transaction=True)
def test_get_recipe_list(client):
    r = client.get('/api/recipes/')
    assert r.status_code == 200


@pytest.mark.django_db(transaction=True)
def test_create_recipe_with_unauth_user(client):
    r = client.post('/api/recipes/')
    assert r.status_code == 401


@pytest.mark.django_db(transaction=True)
def test_create_recipe_with_auth_user(
        auth_client, new_user, ingredient, ingredient_2, tag, tag_2):
    data = {
        'ingredients': [ingredient, ingredient_2],
        'tags': [tag, tag_2],
        'author': new_user,
        'name': 'Банан в шоколаде',
        'image': 'data:image/png;base64,AElFTkSuQmCC',
        'text': 'Непревзойдённый вкус мягкого банана и теплого шоколада',
        'cooking_time': 120
    }

    r = auth_client.post('/api/recipes/', data=data)
    assert r.status_code == 201

    r = auth_client.post('/api/recipes/', data=data)
    assert r.status_code == 400


@pytest.mark.django_db(transaction=True)
def test_get_recipe(client, recipe):
    r = client.get(f'/api/recipes/{recipe.pk}/')
    assert r.status_code == 200

    r = client.get('/api/recipes/999/')
    assert r.status_code == 404


@pytest.mark.django_db(transaction=True)
def test_put_recipe_with_unauth_user(client):
    r = client.put('/api/recipes/999/')
    assert r.status_code == 401


@pytest.mark.django_db(transaction=True)
def test_put_recipe_with_auth_user(auth_client, recipe):
    data = {'name': 'Банан в шоколадном масле', 'cooking_time': 90}
    r = auth_client.put(f'/api/recipes/{recipe.pk}/', data=data)
    assert r.status_code == 200

    data = {'cooking_time': -90}
    r = auth_client.put(f'/api/recipes/{recipe.pk}/', data=data)
    assert r.status_code == 400

    data = {'name': 'Банан в шоколадном масле', 'cooking_time': 90}
    r = auth_client.put('/api/recipes/999/', data=data)
    assert r.status_code == 404


@pytest.mark.django_db(transaction=True)
def test_delete_recipe_with_unauth_user(client):
    r = client.delete('/api/recipes/999/')
    assert r.status_code == 401


@pytest.mark.django_db(transaction=True)
def test_delete_recipe_with_auth_user(auth_client, recipe):
    r = auth_client.delete(f'/api/recipes/{recipe.pk}/')
    assert r.status_code == 204

    r = auth_client.delete(f'/api/recipes/{recipe.pk}/')
    assert r.status_code == 404
