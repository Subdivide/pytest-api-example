from jsonschema import validate, exceptions
from app import PET_STATUS
import sys
import pytest
import schemas
import api_helpers
from hamcrest import assert_that, contains_string, is_

'''
TODO: Finish this test by...
1) Troubleshooting and fixing the test failure
The purpose of this test is to validate the response matches the expected schema defined in schemas.py
'''
def test_pet_schema():
    pet_id = 1
    test_endpoint = f"/pets/{pet_id}"

    response = api_helpers.get_api_data(test_endpoint)

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"

    # Validate the response schema against the defined schema in schemas.py
    try:
        validate(instance=response.json(), schema=schemas.pet)
    except exceptions.ValidationError as e:
        pytest.fail(f"Schema validation failed for pet {pet_id}. {e.message}")

'''
TODO: Finish this test by...
1) Extending the parameterization to include all available statuses
2) Validate the appropriate response code
3) Validate the 'status' property in the response is equal to the expected status
4) Validate the schema for each object in the response
'''
@pytest.mark.parametrize("status", ['available', 'sold', 'pending'])
def test_find_by_status_200(status):
    test_endpoint = "/pets/findByStatus"
    params = {
        "status": status
    }

    matcher = r"^(available|sold|pending){1}"

    response = api_helpers.get_api_data(test_endpoint, params)
    
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    
    pets = response.json()

    for pet in pets:
        assert_that(pet["status"] == status, reason=f'Status validation failed for pet_id {pet["id"]}. Expected status [ {status} ]. Actual status [ {pet["status"]} ]')
        assert_that(pet["status"], reason=f'Status validation failed for pet_id {pet["id"]}. Expected status from [ {" OR ".join(PET_STATUS)} ]. Actual status [ {pet["status"]} ]', matcher=matcher)
        try:
            validate(instance=pet, schema=schemas.pet)
        except exceptions.ValidationError as e:
            pytest.fail(f'Schema validation failed for pet {pet["id"]}. {e.message}')

'''
TODO: Finish this test by...
1) Testing and validating the appropriate 404 response for /pets/{pet_id}
2) Parameterizing the test for any edge cases
'''
@pytest.mark.parametrize("pet_id", [9, 3, -1, 3.14, 3.5 + 5j, "abcd", None, False, sys.maxsize, -sys.maxsize-1])
def test_get_by_id_404(pet_id):
    test_endpoint = f"/pets/{pet_id}"

    response = api_helpers.get_api_data(test_endpoint)

    assert response.status_code == 404
    assert response.headers["Content-Type"] == "application/json"