from src.main import app
import pytest
from httpx import ASGITransport , AsyncClient

BASE_URL="http://localhost:8000"
LONG_URL='https://www.python-httpx.org/quickstart/'
SHORT_URL='krishna123'

@pytest.mark.anyio
async def test_1_create_url():
    async with AsyncClient( transport=ASGITransport(app=app),base_url=BASE_URL) as ac:
        response = await ac.post('/url/shorten',json={'long_url': LONG_URL})
    
    assert response.status_code == 201
    assert response.json() == { "message":"short url successfully created", 
                     "short_url":SHORT_URL,
                     "long_url": LONG_URL,
                     "status":200 }

@pytest.mark.anyio
async def test_2_redirectFunction():
    async with AsyncClient(transport=ASGITransport(app=app),base_url=BASE_URL) as ac:
        response = await ac.get('/url/redirect',params={'short_code':SHORT_URL})
    
    assert response.status_code == 307
    assert response.headers['location'] == LONG_URL
    if response.next_request is not None:
        assert response.next_request.url == LONG_URL

@pytest.mark.anyio
async def test_3_delete_url():
    async with AsyncClient(transport=ASGITransport(app=app),base_url=BASE_URL) as ac:
        response = await ac.delete('/url/', params={'short_code':SHORT_URL})
    
    assert response.status_code == 200
    assert response.json() == {"message":"short_code succesfully deleted"}