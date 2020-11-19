import pytest
import httpx
from config import *

@pytest.mark.asyncio
async def test_as_any_user_fetch_version_resource():
    r = httpx.get(api_url + '/version')
    assert r.status_code == 200
    assert r.text == '{"api": "0.9.1"}'
