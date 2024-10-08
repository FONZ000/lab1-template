import pytest
from app import app, db, Person

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@flask_db:5432/test'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_create_person_success(client):
    response = client.post('/person', json={'name': 'John', 'family': 'Doe', 'email': 'john@example.com'})
    assert response.status_code == 201
    assert response.get_json()['message'] == 'User created'

def test_create_person_invalid_data(client):
    response = client.post('/person', json={'name': 'John', 'family': 'Doe'})
    assert response.status_code == 400
    assert response.get_json()['message'] == 'Invalid input data!'

def test_get_all_people(client):
    client.post('/person', json={'name': 'Jane', 'family': 'Smith', 'email': 'jane@example.com'})
    response = client.get('/person')
    assert response.status_code == 200
    assert len(response.get_json()['people']) == 1

# def test_get_person_by_id_exists(client):
#     client.post('/person', json={'name': 'Jane', 'family': 'Smith', 'email': 'jane@example.com'})
#     response = client.get('/person/1')
#     assert response.status_code == 200
#     assert response.get_json()['person']['name'] == 'Jane'

# def test_delete_person_non_existent(client):
#     response = client.delete('/person/999')
#     assert response.status_code == 404
#     assert response.get_json()['message'] == 'Person not found!'
