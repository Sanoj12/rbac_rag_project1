from fastapi.testclient import TestClient

from app import app
client = TestClient(app)



def test_login():
    client = requests.post(
        f"{API_URL}/auth/login",
        json={
            "email": "sanoj2@gmail.com",
            "password": "sanoj2"
        }
    )

    assert response.status_code ==200



###test add user

def test_add_user():

    client = requests.post(
        f"{API_URL}/admin/add-user",
        json={
            "name": "sano",
            "email": "sano@gmail.com",
            "password": "sano",
            
            "department": "finance"
        },
        headers=headers
    )

    assert response.status_code == 200