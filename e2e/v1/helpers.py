import httpx
from config import *


async def api_admin_auth_headers():
    admin_access_token = await api_access_token(admin_login_name, admin_password)
    return api_auth_header(admin_access_token)


async def api_access_token(login_name, password):
    r = httpx.post(api_url+'/login',
                   json={'login_name': login_name, 'password': password})
    return r.json()['tokens']['access_token']


async def api_get_users():
    admin_auth_header = await api_admin_auth_headers()
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


def get_mentor():
    return {
        "login_name": "mentor1",
        "display_name": "mentor1_nick",
        "password": "mentormentor",
        "email": "mentor1@mentor.mentor",
        "birth_year": 1980,
        "phone": "555-1234",
        "story": "my story",
        "languages": ["fi", "se"],
        "skills": ["vim", "c++", "python"],
        "communication_channels": ["phone", "email"],
        "gender": "other",
        "region": "Tampesteri",
        "role": "mentor"
    }


async def api_create_skill(name, auth_headers):
    return httpx.post(api_url + '/skills', json={'name': name}, headers=auth_headers)


async def api_delete_skills():
    admin_headers = await api_admin_auth_headers()
    skills_r = httpx.get(api_url + '/skills', headers=admin_headers)
    for skill in skills_r.json()['resources']:
        httpx.delete(api_url + '/skills/'+skill['id'], headers=admin_headers)


async def api_create_mentor(mentor):
    admin_headers = await api_admin_auth_headers()
    httpx.post(api_url + '/accounts', headers=admin_headers, json={
        'password': mentor['password'], 'account': {
            'role': mentor['role'], 'login_name': mentor['login_name'],
            'email': mentor['email'], 'phone': mentor['phone']
        }
    })
    mentor_headers = api_auth_header(await api_access_token(mentor['login_name'], mentor['password']))
    myuser = httpx.get(api_url + '/myuser', headers=mentor_headers).json()
    httpx.put(api_url + '/users/'+myuser['user']['id'], headers=mentor_headers, json={
        'display_name': mentor['display_name'], 'birth_year': mentor['birth_year'], 'role': mentor['role'],
        'account_id': myuser['account']['id'], 'id': myuser['user']['id'], 'active': True
    })
    httpx.put(api_url + '/mentors/'+myuser['mentor']['id'], headers=admin_headers, json={
        'birth_year': mentor['birth_year'], 'display_name': mentor['display_name'], 'gender': mentor['gender'],
        'languages': mentor['languages'], 'region': mentor['region'], 'skills': mentor['skills'],
        'story': mentor['story'], 'communication_channels': mentor['communication_channels'],
        'account_id': myuser['account']['id'], 'user_id': myuser['user']['id'], 'id': myuser['mentor']['id']})
