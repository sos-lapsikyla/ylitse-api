import pytest
import httpx
from config import *
from helpers import api_delete_accounts, api_create_mentee_account, get_mentee, api_login, api_access_token, api_auth_header


@pytest.mark.asyncio
async def test_login_as_an_unauthenticated_user():
    await api_delete_accounts()
    mentee = get_mentee()
    await api_create_mentee_account(mentee)

    json = await api_login(mentee)
    assert 'scopes' in json
    assert 'account_id' in json['scopes']
    assert 'user_id' in json['scopes']


@pytest.mark.asyncio
async def test_logout_as_a_logged_in_user():
    await api_delete_accounts()
    mentee = get_mentee()
    await api_create_mentee_account(mentee)

    await api_login(mentee)

    access_token = await api_access_token(mentee['login_name'], mentee['password'])
    auth_header = api_auth_header(access_token)

    r = httpx.get(api_url + '/logout', headers=auth_header)

    assert r.status_code == 200
    json = r.json()
    assert json['message'] == 'Related refresh token invalidated.'
