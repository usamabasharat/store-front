from rest_framework import status
from model_bakery import baker
from store.models import Collection
import pytest


@pytest.fixture
def create_collection(api_client):
  def do_create_collection(collection):
    return api_client.post('/store/collections/', collection)
  return do_create_collection


@pytest.fixture
def update_collection(api_client):
  def do_update_collection(collection_id):
    updated_data = {'title': 'new'}
    return api_client.put(f'/store/collections/{collection_id}/', updated_data)
  return do_update_collection


@pytest.fixture
def delete_collection(api_client):
  def do_delete_collection(collection_id):
    return api_client.delete(f'/store/collections/{collection_id}/')
  return do_delete_collection


@pytest.mark.django_db
class TestCreatCollection:
  def test_if_user_is_anonymous_returns_401(self, create_collection):
    response = create_collection({'title': 'test'})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

  def test_if_user_is_not_admin_returns_403(self, api_client, create_collection, authenticate):
    authenticate()

    response = create_collection({'title': 'test'})

    assert response.status_code == status.HTTP_403_FORBIDDEN

  def test_if_invalid_data_returns_403(self, api_client, create_collection, authenticate):
    authenticate(is_staff=True)

    response = create_collection({'title': ''})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['title'] is not None

  def test_if_valid_data_returns_201(self, api_client, create_collection, authenticate):
    authenticate(is_staff=True)

    response = create_collection({'title': 'test'})

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['id'] > 0


@pytest.mark.django_db
class TestRetrieveCollection:
  def test_if_collection_exist_returns_200(self, api_client):
    collection = baker.make(Collection)

    response = api_client.get(f'/store/collections/{collection.id}/')

    assert response.status_code == status.HTTP_200_OK
    assert response.data == {
        'id': collection.id,
        'title': collection.title,
        'products_count': 0
    }

  def test_if_collection_not_exist_returns_404(self, api_client):
    response = api_client.get(f'/store/collections/1/')

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data is not None


@pytest.mark.django_db
class TestRetrieveCollectionsList:
  def test_if_collections_exist_returns_200(self, api_client):
    collections = baker.make(Collection, _quantity=5)

    response = api_client.get(f'/store/collections/')
    response_data = response.json()
    expected_data = [{'id': col.id, 'title': col.title,
                      'products_count': 0} for col in collections]

    assert response.status_code == status.HTTP_200_OK
    assert response_data == expected_data


@pytest.mark.django_db
class TestUpdateCollection:
  def test_if_user_is_anonymous_returns_401(self, update_collection):
    collection = baker.make(Collection)

    response = update_collection(collection.id)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

  def test_if_user_is_not_admin_returns_403(self, authenticate, update_collection):
    authenticate()
    collection = baker.make(Collection)

    response = update_collection(collection.id)

    assert response.status_code == status.HTTP_403_FORBIDDEN

  def test_if_user_and_data_is_valid_returns_200(self, authenticate, update_collection):
    authenticate(is_staff=True)
    collection = baker.make(Collection)

    response = update_collection(collection.id)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == {
        'id': collection.id,
        'title': 'new',
        'products_count': 0
    }


@pytest.mark.django_db
class TestUpdateCollection:
  def test_if_user_is_anonymous_returns_401(self, update_collection):
    collection = baker.make(Collection)

    response = update_collection(collection.id)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

  def test_if_user_is_not_admin_returns_403(self, authenticate, update_collection):
    authenticate()
    collection = baker.make(Collection)

    response = update_collection(collection.id)

    assert response.status_code == status.HTTP_403_FORBIDDEN

  def test_if_user_and_data_is_valid_returns_200(self, authenticate, update_collection):
    authenticate(is_staff=True)
    collection = baker.make(Collection)

    response = update_collection(collection.id)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == {
        'id': collection.id,
        'title': 'new',
        'products_count': 0
    }


@pytest.mark.django_db
class TestDeleteCollection:
  def test_if_user_is_anonymous_returns_401(self, delete_collection):
    collection = baker.make(Collection)

    response = delete_collection(collection.id)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

  def test_if_user_is_not_admin_returns_403(self, authenticate, delete_collection):
    authenticate()
    collection = baker.make(Collection)

    response = delete_collection(collection.id)

    assert response.status_code == status.HTTP_403_FORBIDDEN

  def test_if_user_and_data_is_valid_returns_200(self, authenticate, delete_collection):
    authenticate(is_staff=True)
    collection = baker.make(Collection)

    response = delete_collection(collection.id)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.data is None
