import pytest
from rest_framework.test import APIClient

from api.models import Ingredient, IngredientInRecipe, Recipe, Tag


@pytest.fixture
@pytest.mark.django_db(transaction=True)
def user(django_user_model):
    return django_user_model.objects.create_user(
        email='9588604@gmail.com',
        username='igorigor',
        first_name='igorigor',
        last_name='markinmarkin',
        password='passwordmarkin'
    )


@pytest.fixture
def api_client():
    client = APIClient()
    client.enforce_csrf_checks = True
    return client


@pytest.fixture
def api_user_client(user, api_client):
    api_client.force_authenticate(user)
    return api_client


@pytest.fixture
def api_user_client_2(new_user_2, api_client):
    api_client.force_authenticate(new_user_2)
    return api_client


@pytest.fixture
@pytest.mark.django_db(transaction=True)
def new_user_2(django_user_model):
    return django_user_model.objects.create(
        email='123456@gmail.com',
        username='harry',
        first_name='harry',
        last_name='potter',
        password='password'
    )


@pytest.fixture
@pytest.mark.django_db(transaction=True)
def ingredient():
    return Ingredient.objects.create(name='Огурец', measurement_unit='шт')


@pytest.fixture
@pytest.mark.django_db(transaction=True)
def ingredient_2():
    return Ingredient.objects.create(name='Соль', measurement_unit='гр')


@pytest.fixture
@pytest.mark.django_db(transaction=True)
def tag():
    return Tag.objects.create(
        name='Завтрак', hex_color='#000000', slug='breakfast')


@pytest.fixture
@pytest.mark.django_db(transaction=True)
def tag_2():
    return Tag.objects.create(name='Обед', hex_color='#eeeeee', slug='lunch')


@pytest.fixture
@pytest.mark.django_db(transaction=True)
def recipe(ingredient, ingredient_2, tag, tag_2, user):
    recipe = Recipe.objects.create(
        author=user,
        name='Огурец с солью',
        image='http://localhost/media/mmm.jpeg',
        text='Вкусный огурец с солью на завтрак и обед',
        cooking_time=1
    )
    recipe.tags.add(tag.pk, tag_2.pk)
    IngredientInRecipe.objects.create(ingredient=ingredient,
                                      recipe=recipe, amount=1)
    IngredientInRecipe.objects.create(ingredient=ingredient_2,
                                      recipe=recipe, amount=1)

    return recipe


@pytest.fixture
def auth_client(client, user):
    client.force_login(user)
    return client
