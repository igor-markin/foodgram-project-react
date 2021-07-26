import pytest
from rest_framework import status


class TestUser:
    @pytest.mark.django_db(transaction=True)
    def test_get_user_list(self, client):
        r = client.get('/api/users/')
        assert r.status_code == status.HTTP_200_OK

    @pytest.mark.django_db(transaction=True)
    def test_user_registration(self, client):
        data = {
            'email': 'igor9588604@gmail.com',
            'username': 'igorigor',
            'first_name': 'igorigor',
            'last_name': 'igormarkin',
            'password': 'passwordigor',
        }
        r = client.post('/api/users/', data=data)
        assert r.status_code == status.HTTP_201_CREATED

    @pytest.mark.django_db(transaction=True)
    def test_user_registration_with_error(self, client):
        data = {
            'email': '9588604@gmail.com',
            'username': 'igor',
        }
        r = client.post('/api/users/', data=data)
        assert r.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.django_db(transaction=True)
    def test_get_user_detail_with_unauth_user(self, api_client, user):
        r = api_client.get(f'/api/users/{user.pk}/')
        assert r.status_code == status.HTTP_200_OK

    @pytest.mark.django_db(transaction=True)
    def test_get_user_detail_with_auth_user(self, api_user_client, user):
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
    def test_get_not_exist_user_detail_with_auth_user(self, api_user_client):
        r = api_user_client.get('/api/users/999/')
        assert r.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.django_db(transaction=True)
    def test_get_me_with_user(self, api_user_client):
        r = api_user_client.get('/api/users/me/')
        assert r.status_code == status.HTTP_200_OK

    @pytest.mark.django_db(transaction=True)
    def test_get_me_with_auth_user(self, api_user_client, user):
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
    def test_change_password_with_unauth_user(self, client):
        r = client.post('/api/users/set_password/')
        assert r.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db(transaction=True)
    def test_change_password_with_auth_user(self, api_user_client):
        data = {
            'new_password': 'new_password*&^%',
            'current_password': 'passwordmarkin'
        }
        r = api_user_client.post('/api/users/set_password/', data=data)
        assert r.status_code == status.HTTP_204_NO_CONTENT

    @pytest.mark.django_db(transaction=True)
    def test_change_password_with_auth_user_with_error(self, api_user_client):
        data = {
            'new_password': 'new_password',
        }
        r = api_user_client.post('/api/users/set_password/', data=data)
        assert r.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.django_db(transaction=True)
    def test_get_token(self, api_client, user):
        data = {
            'password': 'passwordmarkin',
            'email': user.email
        }
        r = api_client.post('/api/auth/token/login/', data=data)
        assert r.status_code == status.HTTP_200_OK

    @pytest.mark.django_db(transaction=True)
    def test_delete_token_with_unauth_user(self, client):
        r = client.post('/api/auth/token/logout/')
        assert r.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db(transaction=True)
    def test_delete_token_with_auth_user(self, api_user_client):
        r = api_user_client.post('/api/auth/token/logout/')
        assert r.status_code == status.HTTP_204_NO_CONTENT

    @pytest.mark.django_db(transaction=True)
    def test_subscriptions_with_unauth_user(self, client):
        r = client.get('/api/users/subscriptions/')
        assert r.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db(transaction=True)
    def test_subscriptions_with_auth_user(self, api_user_client):
        r = api_user_client.get('/api/users/subscriptions/')
        assert r.status_code == status.HTTP_200_OK

    @pytest.mark.django_db(transaction=True)
    def test_subscribe_with_unauth_user(self, api_client, new_user_2):
        r = api_client.get(f'/api/users/{new_user_2.pk}/subscribe/')
        assert r.status_code == status.HTTP_401_UNAUTHORIZED

        r = api_client.delete(f'/api/users/{new_user_2.pk}/subscribe/')
        assert r.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db(transaction=True)
    def test_subscribe_with_auth_user(self, api_user_client, new_user_2):
        r = api_user_client.get(f'/api/users/{new_user_2.pk}/subscribe/')
        assert r.status_code == status.HTTP_201_CREATED

        r = api_user_client.get(f'/api/users/{new_user_2.pk}/subscribe/')
        assert r.status_code == status.HTTP_400_BAD_REQUEST

        r = api_user_client.delete(f'/api/users/{new_user_2.pk}/subscribe/')
        assert r.status_code == status.HTTP_204_NO_CONTENT

        r = api_user_client.delete(f'/api/users/{new_user_2.pk}/subscribe/')
        assert r.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.django_db(transaction=True)
    def test_subscribe_with_auth_user_error(self, api_user_client, user):
        r = api_user_client.get(f'/api/users/{user.pk}/subscribe/')
        assert r.status_code == status.HTTP_201_CREATED

        r = api_user_client.delete(f'/api/users/{user.pk}/subscribe/')
        assert r.status_code == status.HTTP_204_NO_CONTENT

    @pytest.mark.django_db(transaction=True)
    def test_subscribe_with_auth_user_not_found(self, api_user_client):
        r = api_user_client.get(f'/api/users/999/subscribe/')
        assert r.status_code == status.HTTP_404_NOT_FOUND

        r = api_user_client.delete(f'/api/users/999/subscribe/')
        assert r.status_code == status.HTTP_404_NOT_FOUND
