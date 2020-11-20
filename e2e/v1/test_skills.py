import pytest
import httpx
from config import *
from helpers import api_admin_auth_headers, api_auth_header, api_access_token,  \
    api_delete_accounts, api_delete_skills, api_create_skill, get_mentor, \
    api_create_mentor


@pytest.mark.asyncio
async def test_create_a_skill_as_an_admin():
    await api_delete_skills()
    admin_headers = await api_admin_auth_headers()
    r = api_create_skill('vim', admin_headers)
    assert r.status_code == 201
    json = r.json()
    assert 'name' in json
    assert 'id' in json
    assert 'updated' in json
    assert 'created' in json
    assert json['active'] == True


@pytest.mark.asyncio
async def test_get_a_skill_as_an_admin():
    await api_delete_skills()
    admin_headers = await api_admin_auth_headers()
    detox_skill_name = 'detox'
    detox_skill_r = await api_create_skill(detox_skill_name, admin_headers)
    detox_skill_id = detox_skill_r.json()['id']
    skill_r = httpx.get(api_url + '/skills/' +
                        detox_skill_id, headers=admin_headers)
    assert skill_r.json()['name'] == detox_skill_name
    assert skill_r.json()['id'] == detox_skill_id


@pytest.mark.asyncio
async def test_get_all_skills_as_an_admin():
    await api_delete_skills()
    admin_headers = await api_admin_auth_headers()
    detox_skill_name = 'detox'
    pytest_skill_name = 'pytest'
    await api_create_skill(detox_skill_name, admin_headers)
    await api_create_skill(pytest_skill_name, admin_headers)
    skills_r = httpx.get(api_url + '/skills', headers=admin_headers)
    skills = skills_r.json()['resources']
    assert [s for s in skills if s['name'] ==
            detox_skill_name][0]['name'] == detox_skill_name
    assert [s for s in skills if s['name'] ==
            pytest_skill_name][0]['name'] == pytest_skill_name


@pytest.mark.asyncio
async def test_delete_a_skill_as_an_admin():
    await api_delete_skills()
    admin_headers = await api_admin_auth_headers()
    r = api_create_skill('python', admin_headers)
    skill_id = r.json()['id']
    r = httpx.delete(api_url + '/skills/'+skill_id, headers=admin_headers)
    assert r.status_code == 204


@pytest.mark.asyncio
async def test_get_all_skills_as_mentor():
    await api_delete_accounts()
    await api_delete_skills()
    admin_headers = await api_admin_auth_headers()
    detox_skill_name = 'detox'
    pytest_skill_name = 'pytest'
    await api_create_skill(detox_skill_name, admin_headers)
    await api_create_skill(pytest_skill_name, admin_headers)

    mentor = get_mentor()
    await api_create_mentor(mentor)
    mentor_headers = api_auth_header(await api_access_token(mentor['login_name'], mentor['password']))

    skills_r = httpx.get(api_url + '/skills', headers=mentor_headers)
    skills = skills_r.json()['resources']
    assert [s for s in skills if s['name'] ==
            detox_skill_name][0]['name'] == detox_skill_name
    assert [s for s in skills if s['name'] ==
            pytest_skill_name][0]['name'] == pytest_skill_name
