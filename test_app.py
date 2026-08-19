
from sample_app import app


def test_ejemplo():
    client = app.test_client()
    response = client.get('/') 
    
    assert response.status_code == 200