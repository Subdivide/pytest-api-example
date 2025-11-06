from jsonschema import validate, exceptions
from app import PET_TYPE
import pytest
import schemas
import random
import uuid
import api_helpers
from hamcrest import assert_that, contains_string, is_

@pytest.fixture()
def create_pet():
    endpoint = "/pets/"
    params = {
        "id" : uuid.uuid4().int,
        "name" : str(uuid.uuid4().int)[:6],
        "type": random.choice(PET_TYPE),
        "status": "available"
    }

    response = api_helpers.post_api_data(endpoint, params)
    pet = response.json()
    return pet

@pytest.fixture()
def create_order(create_pet):
    endpoint = "/store/order"
    params = {
        "pet_id": create_pet["id"]
    }
    response = api_helpers.post_api_data(endpoint, params)
    order = response.json()
    return order
    

'''
TODO: Finish this test by...
1) Creating a function to test the PATCH request /store/order/{order_id}
2) *Optional* Consider using @pytest.fixture to create unique test data for each run
2) *Optional* Consider creating an 'Order' model in schemas.py and validating it in the test
3) Validate the response codes and values
4) Validate the response message "Order and pet status updated successfully"
'''
@pytest.mark.parametrize("status", ['available', 'sold', 'pending'])
def test_patch_order_by_id(create_order, status):
    test_endpoint = f'/store/order/{create_order["id"]}'
    params = {
        "status": status
    }

    response = api_helpers.patch_api_data(test_endpoint, params)
    
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"

    updated_order = response.json()

    try:
        validate(instance=create_order, schema=schemas.order)
    except exceptions.ValidationError as e:
        pytest.fail(f'Schema validation failed for order {create_order["id"]}. {e.message}')
    
    assert updated_order["message"] == "Order and pet status updated successfully"
