import pytest
from main.policies.house_policy import HousePolicy
from src.main.policies.vehicle_policy import VehiclePolicy

@pytest.fixture
def valid_home_policy_data():
    return {
        "age": 30,
        "flood_risk": "LOW",
        "n_parrots": 0,
        "windows": {"intact": 10, "broken": 0 },
        "outcome": "OK"
    }

@pytest.fixture
def valid_vehicle_policy_data():
    #TODO Implement the valid_vehicle_policy_data fixture
    pass

@pytest.fixture
def invalid_vehicle_policy_data():
    #TODO Implement the invalid_vehicle_policy_data fixture
    pass