import httpx
from config import *


async def api_access_token(login_name, password):
    r = httpx.post(api_url+'/login',
                   json={'login_name': login_name, 'password': password})
    return r.json()['tokens']['access_token']


async def api_get_users():
    admin_access_token = await api_access_token(admin_login_name, admin_password)
    admin_auth_header = api_auth_header(admin_access_token)
    r = httpx.get(api_url + '/users', headers=admin_auth_header)
    return r.json()['resources']


async def api_delete_accounts():
    admin_access_token = await api_access_token(admin_login_name, admin_password)
    admin_auth_header = api_auth_header(admin_access_token)

    for user in await api_get_users():
        if user['role'] == 'admin':
            continue
        httpx.delete(api_url + '/accounts/' +
                     user['account_id'], headers=admin_auth_header)


def api_auth_header(access_token):
    return {
        'Authorization': 'Bearer ' + access_token
    }


async def api_create_mentee_account(mentee):
    httpx.post(api_url+'/accounts', json={'password': mentee['password'], 'account': {
               'role': mentee['role'], 'login_name': mentee['login_name'], 'email': mentee['email']}})
    access_token = await api_access_token(mentee['login_name'], mentee['password'])
    auth_header = api_auth_header(access_token)
    r = httpx.get(api_url + '/myuser', headers=auth_header)
    my_user = r.json()
    r = httpx.put(api_url + '/users/' + my_user['user']['id'], headers=auth_header, json={
                  'display_name': mentee['display_name'], 'role': mentee['role'], 'account_id': my_user['account']['id'], 'id': my_user['user']['id']})

async def api_login(mentee):
    return httpx.post(api_url + '/login',
                   json={'login_name': mentee['login_name'], 'password': mentee['password']}).json()

def get_mentee():
    return {
        'login_name': 'mentee',
        'password': 'menteementee',
        'display_name': 'mentee1',
        'role': 'mentee',
        'email': 'mentee@mentee.mentee'

    }
