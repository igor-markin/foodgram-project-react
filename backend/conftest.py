import pytest
from django.utils import timezone

from recipes.models import Ingredient, Recipe, Tag


@pytest.fixture
def new_user(django_user_model):
    return django_user_model.objects.create(
        email='9588604@gmail.com',
        username='igor',
        first_name='igor',
        last_name='markin',
        password='password'
    )


@pytest.fixture
def new_user_2(django_user_model):
    return django_user_model.objects.create(
        email='123456@gmail.com',
        username='harry',
        first_name='harry',
        last_name='potter',
        password='password'
    )


@pytest.fixture
def ingredient():
    return Ingredient(name='Огурец', measurement_unit='шт')


@pytest.fixture
def ingredient_2():
    return Ingredient(name='Соль', measurement_unit='гр')


@pytest.fixture
def tag():
    return Tag(name='Завтрак', color='#000000', slug='breakfast')


@pytest.fixture
def tag_2():
    return Tag(name='Обед', color='#eeeeee', slug='lunch')


@pytest.fixture
def recipe(ingredient, ingredient_2, tag, tag_2, new_user):
    recipe = Recipe.objects.create(
        author=new_user,
        name='Огурец с солью',
        image='http://localhost/media/mmm.jpeg',
        text='Вкусный огурец с солью на завтрак и обед',
        cooking_time=1,
        pub_date=timezone.now()
    )

    recipe.ingredients.add(*Ingredient.objects.all())
    recipe.tags.add(*Tag.objects.all())

    return recipe


@pytest.fixture
def auth_client(client, new_user):
    client.force_login(new_user)
    return client
