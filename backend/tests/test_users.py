def test_get_user_list(client):
    r = client.get('/api/users/')
    assert r.status_code == 200


def test_user_registration(client):
    data = {
        'email': '9588604@gmail.com',
        'username': 'igor',
        'first_name': 'igor',
        'last_name': 'markin',
        'password': 'password',
    }
    r = client.post('/api/users/', data=data)
    assert r.status_code == 201


def test_user_registration_with_error(client):
    data = {
        'email': '9588604@gmail.com',
        'username': 'igor',
    }
    r = client.post('/api/users/', data=data)
    assert r.status_code == 400


def test_get_user_detail_with_unauth_user(client, new_user):
    r = client.get(f'/api/users/{new_user.pk}/')
    assert r.status_code == 403


def test_get_user_detail_with_auth_user(auth_client, new_user):
    r = auth_client.get(f'/api/users/{new_user.pk}/')
    assert r.json() == {
        "email": new_user.email,
        "id": new_user.pk,
        "username": new_user.username,
        "first_name": new_user.first_name,
        "last_name": new_user.last_name,
        "is_subscribed": 'true',
    }


def test_get_not_exist_user_detail_with_auth_user(auth_client, new_user):
    r = auth_client.get('/api/users/999/')
    assert r.status_code == 404


def test_get_me_with_unauth_user(client):
    r = client.get('/api/users/me/')
    assert r.status_code == 403


def test_get_me_with_auth_user(auth_client, new_user):
    r = auth_client.get('/api/users/me/')
    assert r.json() == {
        "email": new_user.email,
        "id": new_user.pk,
        "username": new_user.username,
        "first_name": new_user.first_name,
        "last_name": new_user.last_name,
        "is_subscribed": 'true',
    }


def test_change_password_with_unauth_user(client):
    r = client.get('/api/users/set_password/')
    assert r.status_code == 403


def test_change_password_with_auth_user(auth_client, new_user):
    data = {
        'new_password': 'new_password',
        'current_password': 'password'
    }
    r = auth_client.post('/api/users/set_password/', data=data)
    assert r.status_code == 201


def test_change_password_with_auth_user_with_error(auth_client, new_user):
    data = {
        'new_password': 'new_password',
    }
    r = auth_client.post('/api/users/set_password/', data=data)
    assert r.status_code == 400


def test_get_token(client, new_user):
    data = {
        'password': new_user.password,
        'email': new_user.email
    }
    r = client.post('/api/auth/token/login/', data=data)
    assert r.status_code == 201


def test_delete_token_with_unauth_user(client):
    r = client.post('/api/auth/token/logout/')
    assert r.status_code == 403


def test_delete_token_with_auth_user(auth_client, new_user):
    r = auth_client.post('/api/auth/token/logout/')
    assert r.status_code == 201


def test_subscriptions_with_unauth_user(client):
    r = client.get('/api/users/subscriptions/')
    assert r.status_code == 403


def test_subscriptions_with_auth_user(auth_client):
    r = auth_client.get('/api/users/subscriptions/')
    assert r.status_code == 200


def test_subscribe_with_unauth_user(client, new_user_2):
    r = client.get(f'/api/users/{new_user_2.pk}/subscribe/')
    assert r.status_code == 403

    r = client.delete(f'/api/users/{new_user_2.pk}/subscribe/')
    assert r.status_code == 403


def test_subscribe_with_auth_user(auth_client, new_user_2):
    r = auth_client.get(f'/api/users/{new_user_2.pk}/subscribe/')
    assert r.status_code == 201

    r = auth_client.get(f'/api/users/{new_user_2.pk}/subscribe/')
    assert r.status_code == 400

    r = auth_client.delete(f'/api/users/{new_user_2.pk}/subscribe/')
    assert r.status_code == 204

    r = auth_client.delete(f'/api/users/{new_user_2.pk}/subscribe/')
    assert r.status_code == 400


def test_subscribe_with_auth_user_error(auth_client, new_user):
    r = auth_client.get(f'/api/users/{new_user.pk}/subscribe/')
    assert r.status_code == 400

    r = auth_client.delete(f'/api/users/{new_user.pk}/subscribe/')
    assert r.status_code == 400


def test_subscribe_with_auth_user_not_found(auth_client):
    r = auth_client.get(f'/api/users/999/subscribe/')
    assert r.status_code == 404

    r = auth_client.delete(f'/api/users/999/subscribe/')
    assert r.status_code == 404
