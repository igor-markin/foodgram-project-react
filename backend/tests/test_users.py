import logging

import pytest


@pytest.mark.django_db(transaction=True)
def test_get_user_list(client):
    r = client.get('/api/users/')
    assert r.status_code == 200


@pytest.mark.django_db(transaction=True)
def test_user_registration(client):
    data = {
        'email': 'igor9588604@gmail.com',
        'username': 'igorigor',
        'first_name': 'igorigor',
        'last_name': 'igormarkin',
        'password': 'passwordigor',
    }
    r = client.post('/api/users/', data=data)
    assert r.status_code == 201


@pytest.mark.django_db(transaction=True)
def test_user_registration_with_error(client):
    data = {
        'email': '9588604@gmail.com',
        'username': 'igor',
    }
    r = client.post('/api/users/', data=data)
    assert r.status_code == 400


@pytest.mark.django_db(transaction=True)
def test_get_user_detail_with_unauth_user(api_client, user):
    r = api_client.get(f'/api/users/{user.pk}/')
    assert r.status_code == 200


@pytest.mark.django_db(transaction=True)
def test_get_user_detail_with_auth_user(api_user_client, user):
    r = api_user_client.get(f'/api/users/{user.pk}/')
    assert r.json() == {
        "email": user.email,
        "id": user.pk,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "is_subscribed": False,
    }


@pytest.mark.django_db(transaction=True)
def test_get_not_exist_user_detail_with_auth_user(api_user_client):
    r = api_user_client.get('/api/users/999/')
    assert r.status_code == 404


@pytest.mark.django_db(transaction=True)
def test_get_me_with_user(api_user_client):
    r = api_user_client.get('/api/users/me/')
    assert r.status_code == 200


@pytest.mark.django_db(transaction=True)
def test_get_me_with_auth_user(api_user_client, user):
    r = api_user_client.get('/api/users/me/')
    assert r.json() == {
        "email": user.email,
        "id": user.pk,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "is_subscribed": False,
    }


@pytest.mark.django_db(transaction=True)
def test_change_password_with_unauth_user(client):
    r = client.post('/api/users/set_password/')
    assert r.status_code == 401


@pytest.mark.django_db(transaction=True)
def test_change_password_with_auth_user(api_user_client):
    data = {
        'new_password': 'new_password*&^%',
        'current_password': 'passwordmarkin'
    }
    r = api_user_client.post('/api/users/set_password/', data=data)
    print(r.content)
    assert r.status_code == 204


@pytest.mark.django_db(transaction=True)
def test_change_password_with_auth_user_with_error(api_user_client):
    data = {
        'new_password': 'new_password',
    }
    r = api_user_client.post('/api/users/set_password/', data=data)
    assert r.status_code == 400


@pytest.mark.django_db(transaction=True)
def test_get_token(api_client, user):
    data = {
        'password': 'passwordmarkin',
        'email': user.email
    }
    r = api_client.post('/api/auth/token/login/', data=data)
    print(user.email, user.password)
    print(r.json())
    assert r.status_code == 200


@pytest.mark.django_db(transaction=True)
def test_delete_token_with_unauth_user(client):
    r = client.post('/api/auth/token/logout/')
    assert r.status_code == 401


@pytest.mark.django_db(transaction=True)
def test_delete_token_with_auth_user(api_user_client):
    r = api_user_client.post('/api/auth/token/logout/')
    assert r.status_code == 204


@pytest.mark.django_db(transaction=True)
def test_subscriptions_with_unauth_user(client):
    r = client.get('/api/users/subscriptions/')
    assert r.status_code == 401


@pytest.mark.django_db(transaction=True)
def test_subscriptions_with_auth_user(api_user_client):
    r = api_user_client.get('/api/users/subscriptions/')
    assert r.status_code == 200


@pytest.mark.django_db(transaction=True)
def test_subscribe_with_unauth_user(api_client, new_user_2):
    r = api_client.get(f'/api/users/{new_user_2.pk}/subscribe/')
    assert r.status_code == 401

    r = api_client.delete(f'/api/users/{new_user_2.pk}/subscribe/')
    assert r.status_code == 401


@pytest.mark.django_db(transaction=True)
def test_subscribe_with_auth_user(api_user_client, new_user_2):
    r = api_user_client.get(f'/api/users/{new_user_2.pk}/subscribe/')
    assert r.status_code == 201

    r = api_user_client.get(f'/api/users/{new_user_2.pk}/subscribe/')
    assert r.status_code == 400

    r = api_user_client.delete(f'/api/users/{new_user_2.pk}/subscribe/')
    assert r.status_code == 204

    r = api_user_client.delete(f'/api/users/{new_user_2.pk}/subscribe/')
    assert r.status_code == 404


@pytest.mark.django_db(transaction=True)
def test_subscribe_with_auth_user_error(api_user_client, user):
    r = api_user_client.get(f'/api/users/{user.pk}/subscribe/')
    assert r.status_code == 201

    r = api_user_client.delete(f'/api/users/{user.pk}/subscribe/')
    assert r.status_code == 204


@pytest.mark.django_db(transaction=True)
def test_subscribe_with_auth_user_not_found(api_user_client):
    r = api_user_client.get(f'/api/users/999/subscribe/')
    assert r.status_code == 404

    r = api_user_client.delete(f'/api/users/999/subscribe/')
    assert r.status_code == 404
